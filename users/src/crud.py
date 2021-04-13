from typing import List, Optional

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product


async def get_all_products(session: AsyncSession) -> List[Product]:
    products = await session.execute(select(Product))
    return products.scalars().all()


async def get_product(session: AsyncSession, id: int):
    product = await session.execute(select(Product).where(Product.id == id))
    return product.scalar()


async def create_product(session: AsyncSession, id: int, title: str, image: str):
    product = insert(Product).values(id=id, title=title, image=image)
    await session.execute(product)
    await session.commit()


async def update_product(session: AsyncSession, id: int, title: Optional[str],
                         image: Optional[str], likes: Optional[int]):
    product = update(Product).where(Product.id == id).values(title=title, image=image, likes=likes)
    product.execution_options(synchronize_session="fetch")
    await session.execute(product)
    await session.commit()


async def delete_product(session: AsyncSession, id: int):
    product = delete(Product).where(Product.id == id)
    await session.execute(product)
    await session.commit()
