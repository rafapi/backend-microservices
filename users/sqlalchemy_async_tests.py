import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert, select
from sqlalchemy.orm import sessionmaker

from src.models import Product


DATABASE_URL = "postgresql+asyncpg://root:root@localhost:35432/main"
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)
Base = declarative_base()
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session():
    async with async_session() as session:
        async with session.begin():
            return ProductDAL(session)


class ProductDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, id, title, image):
        product = insert(Product).values(id=id, title=title, image=image)
        await self.session.execute(product)
        await self.session.commit()

    async def get_all(self):
        products = await self.session.execute(select(Product))
        await self.session.commit()
        return products.scalars().all()


async def create(id: int, title: str, image: str):
    session = await get_session()
    return await session.create(id, title, image)


async def get_all():
    session = await get_session()
    return await session.get_all()


# asyncio.run(create(5, 'hello', 'pretty image'))
asyncio.run(get_all())
