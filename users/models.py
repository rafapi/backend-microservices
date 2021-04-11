from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from main import app


db_u = SQLAlchemy(app)


@dataclass
class Product(db_u.Model):
    id: int = db_u.Column(db_u.Integer, primary_key=True, autoincrement=False)
    title: str = db_u.Column(db_u.String(200))
    image: str = db_u.Column(db_u.String(200))
    likes: int = db_u.Column(db_u.Integer, autoincrement=False, default=0)


@dataclass
class ProductUser(db_u.Model):
    id = db_u.Column(db_u.Integer, primary_key=True)
    user_id = db_u.Column(db_u.Integer)
    product_id = db_u.Column(db_u.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')
