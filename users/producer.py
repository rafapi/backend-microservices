import asyncio
import logging
import json

from aio_pika import connect_robust, Message, ExchangeType

# from pika.exceptions import StreamLostError


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


async def publish(content_type, body):
    connection = await connect_robust(
        "amqp://guest:guest@rabbitmq:5672/products"
    )

    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        "products", ExchangeType.DIRECT, durable=True
    )

    message_body = bytes(json.dumps(body), 'utf-8')

    message = Message(body=message_body,
                      content_type=content_type
                      )

    await exchange.publish(message, routing_key='admin')

    print(" [x] Sent %r" % message.body)

    await connection.close()
