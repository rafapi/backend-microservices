import asyncio
from aio_pika import connect_robust, Message, ExchangeType


async def main(loop):
    # Perform connection
    connection = await connect_robust(
        "amqp://guest:guest@rabbitmq:5672/products", loop=loop
    )

    # Creating a channel
    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        "products", ExchangeType.DIRECT, durable=True
        )

    # Sending the message
    message_body = b'4'
    message = Message(message_body)
    await exchange.publish(message, routing_key="admin")

    print(" [x] Sent %r" % message)

    await connection.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
