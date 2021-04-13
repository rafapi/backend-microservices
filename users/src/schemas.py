from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: int
    title: str
    image: str
    likes: int
