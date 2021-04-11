import logging
import json
import threading
import pika

from functools import partial

from models import Product, db_u


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


def ack_message(ch, delivery_tag):
    if ch.is_open:
        ch.basic_ack(delivery_tag)
    else:
        LOGGER.debug('Channel already closed!')


def process_data(connection, ch, properties, delivery_tag, body):
    LOGGER.debug('Received in main')

    data = json.loads(body)
    LOGGER.debug(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db_u.session.add(product)
        db_u.session.commit()
        LOGGER.debug('Product Created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db_u.session.commit()
        LOGGER.debug('Product Updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db_u.session.delete(product)
        db_u.session.commit()
        LOGGER.debug('Product Deleted')

    cb = partial(ack_message, ch, delivery_tag)
    connection.add_callback_threadsafe(cb)


def on_message(ch, method_frame, properties, body, args):
    (connection, threads) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=process_data, args=(connection, ch, properties, delivery_tag, body))
    t.start()
    threads.append(t)


LOGGER.debug("Connecting...")
credentials = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(host='rabbitmq', port=5672,
                                   virtual_host='products', credentials=credentials)
connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.exchange_declare(exchange="products", exchange_type="direct", passive=False,
                         durable=True, auto_delete=False)
channel.queue_declare(queue='main', auto_delete=True)
channel.queue_bind(queue='main', exchange="products", routing_key='main')
channel.basic_qos(prefetch_count=1)

threads = []
process_data_callback = partial(on_message, args=(connection, threads))
channel.basic_consume(queue='main', on_message_callback=process_data_callback)

try:
    print('Started Consuming')
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()
