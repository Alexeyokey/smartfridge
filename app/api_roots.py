from flask import Blueprint, jsonify
# from ..setting_param import COUNT_PAGE
from app.bd.database import Product
api = Blueprint('api', __name__, template_folder="templates")
COUNT_PAGE  = 2
@api.route('/product', methods=['GET'])
def test():
    return jsonify({'message': "API is working!"})


@api.route('/products/<int:page>', methods=['GET'])
def test2(page):
    products = Product.select().where(Product.id > (page - 1) * COUNT_PAGE).limit(COUNT_PAGE)
    # select * from products WHERE id > (page - 1) * COUNT_PAGE LIMIT COUNT_PAGE
    return jsonify({'products': [{'id': obj.id, 'name': obj.name, 'type': obj.type, 'price': obj.price} for obj in products]})