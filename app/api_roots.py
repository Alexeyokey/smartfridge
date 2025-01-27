from flask import Blueprint, jsonify, request
from datetime import timedelta, datetime
from app import COUNT_PAGE
import requests
from app.bd.database import Product
from app.bd.database import QR
from app.bd.database import Fridge

api = Blueprint('api', __name__, template_folder="templates")

@api.route('/product', methods=['GET'])
def test():
    return jsonify({'message': "API is working!"})


@api.route('/qr_products/<int:page>', methods=['GET']) # тестрирование апи на работоспособность, отправка ограниченного количества продуктов на стриницу
def get_qr_products_limit(page):
    products = QR.select().where(QR.id > (page - 1) * COUNT_PAGE).order_by(QR.last_date).limit(COUNT_PAGE)
    # select * from products WHERE id > (page - 1) * COUNT_PAGE LIMIT COUNT_PAGE
    expired_products = {}
    for obj in products:
        if datetime.now() > obj.last_date:
            expired_products[obj.id] = True 
        else:
            expired_products[obj.id] = False
    return jsonify({'products': [{'id': obj.id, 'name': obj.product.name, 'type': obj.product.type, 'price': obj.price, 'count': obj.count, 'produced_date': obj.produced_date, 'last_date': obj.last_date, 'expired': expired_products[obj.id]} for obj in products]})

@api.route('/products/', methods=['GET']) # тестрирование апи на работоспособность, отправка ограниченного количества продуктов на стриницу
def get_products():
    products = Product.select()
    # select * from products WHERE id > (page - 1) * COUNT_PAGE LIMIT COUNT_PAGE
    # print(products)
    # for i in products:
    #     products(i.product.name)
    return jsonify({'products': [{'id': obj.id, 'name': obj.name, 'type': obj.type, 'ingredients': obj.ingredients, 'allergic': obj.allergic} for obj in products]})

@api.route('/expired_count', methods=['GET'])
def expired_count():
    count = QR.select().where(QR.last_date < datetime.now()).count()
    # select COUNT* from products WHERE id > (page - 1) * COUNT_PAGE LIMIT COUNT_PAGE
    return jsonify({'count': count})


@api.route('/product/<int:id>', methods=['GET']) # тестрирование апи на работоспособность, отправка ограниченного количества продуктов на стриницу
def get_product(id):
    products = QR.select().where(QR.id == id)
    # select * from products WHERE id > (page - 1) * COUNT_PAGE LIMIT COUNT_PAGE
    return jsonify({'products': [{'id': obj.id, 'name': obj.product.name, 'type': obj.product.type, 'price': obj.price, 'count': obj.count, 'produced_date': obj.produced_date, 'last_date': obj.last_date} for obj in products]})

@api.route('/product/<int:id>', methods=['DELETE']) # тестрирование апи на работоспособность, отправка ограниченного количества продуктов на стриницу
def delete(id):
    # print(id)
    product = QR.get(QR.id == str(id))
    product.delete_instance()
    # select * from products WHERE id > (page - 1) * COUNT_PAGE LIMIT COUNT_PAGE
    return jsonify({'msg': 'deleted'})

@api.route('/add_qr_product', methods=['POST']) # тестрирование апи на работоспособность, отправка ограниченного количества продуктов на стриницу
def add_qr_product():
    print('!!!!!')
    # print(request.json.keys())
    qr_id = request.json.get('qr_id')
    data = {
            'product': qr_id
        }
    Fridge.create(**data)
    # print(qr_id)
    # product = request.json.get('product')
    # product = request.json.get('product')
    # print(product.json())
    # QR.create(*product_inf)
    return jsonify({'msg': 'added'})


@api.route('/history/<int:page>', methods=['GET'])
def get_shopping_history(page):
    products = QR.select().where(QR.id > (page - 1) * COUNT_PAGE).limit(COUNT_PAGE)
    # select * from products WHERE id > (page - 1) * COUNT_PAGE LIMIT COUNT_PAGE
    expired_products = []
    for obj in products:
        if datetime.now() > obj.last_date:
            expired_products.append(True)
        else:
            expired_products.append(False)
    print(expired_products)
    return jsonify({'products': [{'id': obj.id, 'name': obj.product.name, 'type': obj.product.type, 
                                  'price': obj.price, 'count': obj.count, 'produced_date': obj.produced_date, 
                                  'last_date': obj.last_date, 'expired': expired_products[obj.id]} ]})

