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
    return jsonify({'products': [{'id': obj.id, 'name': obj.name, 'type': obj.type, 'ingredients': obj.ingredients, 'allergic': obj.allergic} for obj in products]})


##### Работа с БД QR #####
# код для работы с таблицей QR
@api.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    products = QR.select().where(QR.id == id)
    # select * from products WHERE id > (page - 1) * COUNT_PAGE LIMIT COUNT_PAGE
    return jsonify({'products': [{'id': obj.id, 'name': obj.product.name, 'type': obj.product.type, 'price': obj.price, 
                                  'count': obj.count, 'produced_date': obj.produced_date, 'last_date': obj.last_date, 'allergic': obj.product.allergic} for obj in products]})

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
          expired_products[obj.id] = datetime.now() > obj.last_date
    return jsonify({'products': [{'id': obj.id, 'name': obj.product.name, 'type': obj.product.type, 'calories': obj.calories, 'price': obj.price, 'count': obj.count, 'produced_date': obj.produced_date, 'last_date': obj.last_date, 'expired': expired_products[obj.id]} for obj in products]})

# код для работы с таблицей QR
@api.route('/product/<int:id>', methods=['DELETE'])
def delete(id):
    product = QR.get(QR.id == str(id))
    product.delete_instance()
    return jsonify({'msg': 'deleted'})


# код для работы с таблицей QR
@api.route('/expired_count', methods=['GET'])
def expired_count():
    count = QR.select().where(QR.last_date < datetime.now()).count()
    return jsonify({'count': count})

##### Работа с БД ShoppingListHistory #####
# код для работы с таблицей ShoppingListHistory
@api.route('/history/<int:page>', methods=['GET'])
def get_shopping_history(page):
    products = ShoppingListHistory.select().where(QR.id > (page - 1) * COUNT_PAGE).limit(COUNT_PAGE)
    return jsonify({'products': [{'id': obj.id, 'name': obj.product.name, 'quantity': obj.quantity}  for obj in products]})

# код для работы с таблицей ShoppingListHistory
@api.route('/history', methods=['POST'])
def add_shopping_history():
    qr_id = request.json.get('qr_id')
    quantity = request.json.get('quantity')
    data = {
            'product': qr_id,
            'quantity': quantity
        }
    
    history = ShoppingListHistory.create(**data)
    return jsonify({'msg': 'added'})


# код для работы с таблицей ShoppingListHistory
@api.route('/history', methods=['DELETE'])
def delete_shopping_history(id):
    history = ShoppingListHistory.get(ShoppingListHistory.id == str(id))
    history.delete_instance()
    return jsonify({'msg': 'deleted'})


##### Работа с БД Storage #####
# код для работы с таблицей Storage
@api.route('/add_qr_product', methods=['POST'])
def add_qr_product():
    qr_id = request.json.get('qr_id')
    data = {
            'product': qr_id
        }
    Storage.create(**data)
    return jsonify({'msg': 'added'})



