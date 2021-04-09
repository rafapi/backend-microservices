import logging
import os
import json
import threading

import pika
import django

from functools import partial


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


def ack_message(ch, delivery_tag):
    if ch.is_open:
        ch.basic_ack(delivery_tag)
    else:
        LOGGER.debug('Channel already closed!')


def process_data(connection, ch, delivery_tag, body):
    LOGGER.debug('Received in admin')
    id = json.loads(body)
    LOGGER.debug(id)
    product = Product.objects.get(id=id)
    product.likes += 1
    product.save()
    LOGGER.debug('Product likes increased.')
    cb = partial(ack_message, ch, delivery_tag)
    connection.add_callback_threadsafe(cb)


def on_message(ch, method_frame, header_frame, body, args):
    (connection, threads) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=process_data, args=(connection, ch, delivery_tag, body))
    t.start()
    threads.append(t)


LOGGER.debug("Connecting...")
credentials = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='products',
                                   credentials=credentials)
connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.exchange_declare(exchange="products", exchange_type="direct", passive=False,
                         durable=True, auto_delete=False)

channel.queue_declare(queue='admin', auto_delete=True)
channel.queue_bind(queue='admin', exchange="products", routing_key='admin')
channel.basic_qos(prefetch_count=1)

threads = []
process_data_callback = partial(on_message, args=(connection, threads))
channel.basic_consume(queue='admin', on_message_callback=process_data_callback)

LOGGER.debug('Started Consuming')

channel.start_consuming()

channel.close()
