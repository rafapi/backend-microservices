from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product


async def get_all(session: AsyncSession) -> list[Product]:
    products = select(Product)
    return await session.execute(products)


async def post_like(session: AsyncSession, id: int):
    product = await session.execute(select(Product).where(Product.id == id))
    session.add(product)
    return product

def post(session: AsyncSession, id: int, title: str, image: str):
    product = Product(id=id, title=title, image=image)
    session.add(product)
    return product
