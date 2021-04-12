import asyncio
# import requests
import typer

from typing import List

from fastapi import FastAPI, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from src.db.base import init_models
from src.db.base import get_session
from src import crud


app = FastAPI()
cli = typer.Typer()


class ProductSchema(BaseModel):
    id: int
    title: str
    image: str
    likes: int


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")


@app.get("/api/products")
async def get_products(session: AsyncSession = Depends(get_session)) -> List[ProductSchema]:
    return await crud.get_all(session)


@app.post("/api/products/{id}/like")
async def like(id: int = Path(..., gt=0), session: AsyncSession = Depends(get_session)):
    # req = requests.get('http://localhost:8000/api/user')
    # data = req.json()

    product = await crud.like(session, id)
    print(f"QUERY: {product}")
    try:
        await session.commit()
        return {"product": id, "message": "success"}
    except IntegrityError as ex:
        await session.rollback()
        raise Exception(f"You already liked this product: {ex}")


@app.post("/api/products/")
async def create_product(product: ProductSchema, session: AsyncSession = Depends(get_session)):
    await crud.create_product(session, product.id, product.title, product.image)

    response_obj = {"title": product.title, "image": product.image}

    return response_obj


if __name__ == "__main__":
    cli()
