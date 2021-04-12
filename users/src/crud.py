from typing import List, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product


async def get_all(session: AsyncSession) -> List[Product]:
    products = await session.execute(select(Product))
    return products.scalars().all()


async def like(session: AsyncSession, id: int):
    product = await session.execute(select(Product).where(Product.id == id))
    session.add(product)
    await session.flush()


async def create_product(session: AsyncSession, id: int, title: str, image: str):
    product = Product(id=id, title=title, image=image)
    session.add(product)
    await session.commit()


async def update_product(session: AsyncSession, title: Optional[str], image: Optional[str]):
    product = update(Product).where(Product.id == id).values(title=title, image=image)
    product.execution_options(synchronize_session="fetch")
    await session.execute(product)


async def delete_product(session: AsyncSession, id: int):
    product = delete((Product).where(Product.id == id))
    await session.execute(product)
