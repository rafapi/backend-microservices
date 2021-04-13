import logging
import json
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from aio_pika import connect_robust, ExchangeType, IncomingMessage

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

    session: AsyncSession = await get_session()

    async with message.process():
        data = json.loads(message.body)
        LOGGER.debug(data)

        if message.content_type == 'product_created':
            await crud.create_product(session, id=data['id'], title=data['title'], image=data['image'])
            LOGGER.debug('Product Created (async)')

        elif message.content_type == 'product_updated':
            await crud.update_product(session, id=data['id'], title=data['title'],
                                      image=data['image'], likes=data['likes'])
            LOGGER.debug('Product Updated')

        elif message.content_type == 'product_deleted':
            await crud.delete_product(session, id=int(data))
            LOGGER.debug('Product Deleted')


async def main(loop):
    LOGGER.debug('Receiving messages in main')
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
    LOGGER.debug(" [*] Waiting for messages...")
    loop.run_forever()
except KeyboardInterrupt:
    LOGGER.debug("Interrupted by user")
