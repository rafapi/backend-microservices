from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

from .db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=False, index=True)
    title = Column(String(200))
    image = Column(String(200))
    likes = Column(Integer, default=0)
