from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from app import COUNT_PAGE
from app.bd.database import Storage, ShoppingListHistory, QR, Product
from .bd_functions import *


api = Blueprint('api', __name__, template_folder="templates")

##### Работа с БД Product #####
# код для работы с таблицей Product
@api.route('/products/', methods=['GET']) 
def get_products():
    products = Product.select()
    return jsonify({'products': [{'id': obj.id, 'name': obj.name, 'type': obj.type, 'calories': obj.calories, 'ingredients': obj.ingredients, 'allergic': obj.allergic} for obj in products]})


##### Работа с БД QR #####
# код для работы с таблицей QR
@api.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    obj = QR.get(QR.id == str(id))
    # select * from products WHERE id > (page - 1) * COUNT_PAGE LIMIT COUNT_PAGE
    return jsonify({'product': {'id': obj.id, 'name': obj.product.name, 'type': obj.product.type, 'price': obj.price, 'product_id': obj.product.id,
                                  'measurement': obj.measurement, 'type_measurement': obj.type_measurement, 'produced_date': obj.produced_date, 'last_date': obj.last_date, 'allergic': obj.product.allergic}})


# код для работы с таблицей QR
@api.route('/qr_products/<int:page>', methods=['GET'])
def get_qr_products_limit(page):
    return jsonify(bd_get_qr_products(page))

# код для работы с таблицей QR
@api.route('/product/<int:id>', methods=['DELETE'])
def product_delete(id):
    product = QR.get(QR.id == str(id))
    # product.delete_instance()
    product.deleted = True
    product.deleted_date = datetime.now()
    product.save()
    return jsonify({'msg': 'deleted'})


##### Работа с БД ShoppingListHistory #####
# код для работы с таблицей ShoppingListHistory
@api.route('/shopping_list', methods=['GET'])
def get_shopping_history():
    products = bd_get_shopping_history
    return jsonify(products)


# код для работы с таблицей ShoppingListHistory
@api.route('/shopping_list/<int:id>', methods=['DELETE'])
def delete_shopping_history(id):
    history = ShoppingListHistory.get(ShoppingListHistory.id == str(id))
    history.deleted = True
    history.deleted_date = datetime.now()
    history.save()
    return jsonify({'msg': 'deleted'})


##### Работа с БД Storage #####
# код для работы с таблицей Storage
@api.route('/add_qr_product_storage', methods=['POST'])
def add_storage_product():
    qr_id = request.json.get('qr_id')
    data = {
            'qr_product': qr_id 
        }
    Storage.create(**data)
    return jsonify({'msg': 'added'})

# код для работы с таблицей Storage
@api.route('/expired_count', methods=['GET'])
def expired_count():
    count = bd_expired_count()
    return jsonify({'count': count})

# код для работы с таблицей Storage
@api.route('/soon_expire', methods=['GET'])
def soon_expire():
    print(datetime.now() - timedelta(days=7))
    return '1'
    # count = Storage.select(Storage).join(QR, on=(Storage.qr_product == QR.id)).where((QR.last_date < datetime.now()) & (Storage.deleted == 0)).count()
    # return jsonify({'count': count})

# код для работы с таблицей Storage
@api.route('/storage/<int:page>', methods=['GET'])
def get_storage_products_limit(page):
   return jsonify(bd_get_storage_product(id))

# код для работы с таблицей Storage
@api.route('/storage/<int:id>', methods=['DELETE'])
def storage_delete(id):
    product = Storage.get(Storage.id == str(id))
    # product.delete_instance()
    product.deleted = True
    product.deleted_date = datetime.now()
    product.save()
    return jsonify({'msg': 'deleted'})

