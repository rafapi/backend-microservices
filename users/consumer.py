import logging
import json
import asyncio

from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from aio_pika import connect_robust, ExchangeType, IncomingMessage

from src.models import Product
from src import crud


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


DATABASE_URL = "postgresql+asyncpg://root:root@fast-db/main"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            return session


async def process_message(message: IncomingMessage):
    async with message.process():
        data = json.loads(message.body)
        print(data['title'])
        print(data['image'])
        await asyncio.sleep(1)


async def process_data(message: IncomingMessage):
    LOGGER.debug('Received in main')
    print('Received in main')

    session: AsyncSession = await get_session()
    print(session)

    async with message.process():
        data = json.loads(message.body)
        print(data['title'])
        print(data['image'])
        LOGGER.debug(data)

        if message.content_type == 'product_created':
            await crud.create_product(session, id=data['id'], title=data['title'], image=data['image'])
            LOGGER.debug('Product Created')
            print('Product Created')

        elif message.content_type == 'product_updated':
            await crud.update_product(session, title=data['title'], image=data['image'])
            LOGGER.debug('Product Updated')
            print('Product Updated')

        elif message.content_type == 'product_deleted':
            await crud.update_product(session, id=data['id'])
            LOGGER.debug('Product Deleted')
            print('Product Deleted')


async def main(loop):
    print('Receiving messages in main')
    connection = await connect_robust(
        "amqp://guest:guest@rabbitmq:5672/products", loop=loop
    )

    # Creating channel
    channel = await connection.channel()

    # Maximum message count which will be
    # processing at the same time.
    await channel.set_qos(prefetch_count=1)

    exchange = await channel.declare_exchange(
        "products", ExchangeType.DIRECT, durable=True
    )

    # Declaring queue
    queue = await channel.declare_queue('main', auto_delete=True)

    await queue.bind(exchange)

    await queue.consume(process_data)


loop = asyncio.get_event_loop()
loop.create_task(main(loop))

try:
    print(" [*] Waiting for messages. To exit press CTRL+C")
    loop.run_forever()
except KeyboardInterrupt:
    print("Interrupted by user")
