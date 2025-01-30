from flask import Blueprint, jsonify, request
from datetime import datetime
from app import COUNT_PAGE
from app.bd.database import Storage, ShoppingListHistory, QR, Product


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
                                  'count': obj.count, 'produced_date': obj.produced_date, 'last_date': obj.last_date, 'allergic': obj.product.allergic}})


# код для работы с таблицей QR
@api.route('/qr_products/<int:page>', methods=['GET'])
def get_qr_products_limit(page):
    """Извлекает разбитый на страницы список QR-продуктов.
    
        Аргументы:
        page (int): номер страницы, для которой нужно выбрать товары.
        
        Возвращает:ответ в формате JSON,
        содержащий список продуктов с их подробной информацией, включая статус истечения срока годности.
    """
    products = QR.select().where(QR.id > (page - 1) * COUNT_PAGE).order_by(QR.last_date).limit(COUNT_PAGE)
    # select * from products WHERE id > (page - 1) * COUNT_PAGE LIMIT COUNT_PAGE
    expired_products = {}
    for obj in products:
          if not obj.deleted:
            expired_products[obj.id] = datetime.now() > obj.last_date
    return jsonify({'products': [{'id': obj.id, 'name': obj.product.name, 'type': obj.product.type, 'price': obj.price, 'count': obj.count, 'produced_date': obj.produced_date, 'last_date': obj.last_date, 'expired': expired_products[obj.id]} for obj in products]})

# код для работы с таблицей QR
@api.route('/product/<int:id>', methods=['DELETE'])
def product_delete(id):
    product = QR.get(QR.id == str(id))
    # product.delete_instance()
    product.deleted = True
    product.deleted_date = datetime.now()
    product.save()
    return jsonify({'msg': 'deleted'})



# код для работы с таблицей QR
@api.route('/expired_count', methods=['GET'])
def expired_count():

    count = QR.select().where(QR.last_date < datetime.now(), not QR.deleted).count()
    return jsonify({'count': count})


##### Работа с БД ShoppingListHistory #####
# код для работы с таблицей ShoppingListHistory
@api.route('/shopping_list', methods=['GET'])
def get_shopping_history():
    products = ShoppingListHistory.select()

    return jsonify({'products': [{'id': obj.id, 'name': obj.product.name, 'quantity': obj.quantity}  for obj in products if not obj.deleted]})


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
@api.route('/add_qr_product', methods=['POST'])
def add_storage_product():
    qr_id = request.json.get('qr_id')
    data = {
            'qr_product': qr_id 
        }
    Storage.create(**data)
    return jsonify({'msg': 'added'})

# код для работы с таблицей Storage
@api.route('/storage/<int:page>', methods=['GET'])
def get_storage_products_limit(page):
    """Извлекает разбитый на страницы список продуктов в холодильнике.
    
        Аргументы:
        page (int): номер страницы, для которой нужно выбрать товары.
        
        Возвращает:ответ в формате JSON,
        содержащий список продуктов с их подробной информацией, включая статус истечения срока годности.
    """
    # print(Storage.qr_product.last_date)
    products = Storage.select(Storage).join(QR, on=(Storage.qr_product == QR.id)).where(Storage.id > (page - 1) * COUNT_PAGE).order_by(QR.last_date).limit(COUNT_PAGE)
    
    # select * from products WHERE id > (page - 1) * COUNT_PAGE LIMIT COUNT_PAGE
    expired_products = {}
    for obj in products:
          if not obj.deleted:
            expired_products[obj.id] = datetime.now() > obj.qr_product.last_date
    
    return jsonify({'products': [{'id': obj.id, 'name': obj.qr_product.product.name, 'calories': obj.qr_product.product.calories, 'type': obj.qr_product.product.type, 
                                  'price': obj.qr_product.price, 'count': obj.qr_product.count, 'produced_date': obj.qr_product.produced_date, 'last_date': obj.qr_product.last_date, 
                                  'expired': expired_products[obj.id]} for obj in products if not obj.deleted]})


# код для работы с таблицей QR
@api.route('/storage/<int:id>', methods=['DELETE'])
def storage_delete(id):
    product = Storage.get(Storage.id == str(id))
    # product.delete_instance()
    product.deleted = True
    product.deleted_date = datetime.now()
    product.save()
    return jsonify({'msg': 'deleted'})

