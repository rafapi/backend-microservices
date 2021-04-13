import logging
import json
import threading
import pika

from functools import partial

from sqlalchemy.ext.asyncio import AsyncSession
from pika.adapters.asyncio_connection import AsyncioConnection

from src import crud
from src.db.base import get_session


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


def ack_message(ch, delivery_tag):
    if ch.is_open:
        ch.basic_ack(delivery_tag)
    else:
        LOGGER.debug('Channel already closed!')


async def process_data(connection, ch, properties, delivery_tag, body):
    LOGGER.debug('Received in main')
    print('Received in main')

    data = json.loads(body)
    LOGGER.debug(data)

    session: AsyncSession = get_session()

    if properties.content_type == 'product_created':
        await crud.create_product(session, data['id'], data['title'], data['image'])
        LOGGER.debug('Product Created')
        print('Product Created')

    elif properties.content_type == 'product_updated':
        await crud.update_product(session, data['title'], data['image'])
        LOGGER.debug('Product Updated')
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        await crud.delete_product(session, data['id'])
        LOGGER.debug('Product Deleted')
        print('Product Deleted')

    cb = partial(ack_message, ch, delivery_tag)
    await connection.add_callback_threadsafe(cb)


async def on_message(ch, method_frame, properties, body):
    delivery_tag = method_frame.delivery_tag
    await process_data(connection, ch, properties, delivery_tag, body)


LOGGER.debug("Connecting...")
credentials = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(host='rabbitmq', port=5672,
                                   virtual_host='products', credentials=credentials)
connection = AsyncioConnection(params)

channel = connection.channel()
channel.exchange_declare(exchange="products", exchange_type="direct", passive=False,
                         durable=True, auto_delete=False)
channel.queue_declare(queue='main', auto_delete=True)
channel.queue_bind(queue='main', exchange="products", routing_key='main')
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='main', on_message_callback=on_message)

try:
    print('Started Consuming')
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()
