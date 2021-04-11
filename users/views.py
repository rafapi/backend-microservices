import requests

from flask import jsonify, abort
from werkzeug.exceptions import HTTPException

from producer import publish
from main import app
from models import db_u, Product, ProductUser


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['GET', 'POST'])
def like(id):
    req = requests.get('http://172.17.0.1:8000/api/user')
    data = req.json()

    try:
        product_user = ProductUser(user_id=data['id'], product_id=id)
        product = Product.query.filter_by(id=id).first()
        product.likes += 1
        db_u.session.add(product_user)
        db_u.session.commit()

        publish('product_liked', id)

    except HTTPException:
        abort(400, 'You already liked this product.')

    return jsonify({
        'message': 'success'
        })
