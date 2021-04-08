import requests

from dataclasses import dataclass

from flask import Flask, jsonify, abort
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint

from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db_u/main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

CORS()

db_u = SQLAlchemy(app)


@dataclass
class Product(db_u.Model):
    id: int = db_u.Column(db_u.Integer, primary_key=True, autoincrement=False)
    title: str = db_u.Column(db_u.String(200))
    image: str = db_u.Column(db_u.String(200))


@dataclass
class ProductUser(db_u.Model):
    id = db_u.Column(db_u.Integer, primary_key=True)
    user_id = db_u.Column(db_u.Integer)
    product_id = db_u.Column(db_u.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['GET', 'POST'])
def like(id):
    req = requests.get('http://172.17.0.1:8000/api/user')
    json = req.json()

    try:
        product_user = ProductUser(user_id=json['id'], product_id=id)
        db_u.session.add(product_user)
        db_u.session.commit()

        publish('product_liked', id)

    except HTTPException:
        abort(400, 'You already liked this product.')

    return jsonify({
        'message': 'success'
        })
