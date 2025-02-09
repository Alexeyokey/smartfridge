from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from app import COUNT_PAGE
from app.bd.database import Storage, ShoppingListHistory, QR, Product
from .bd_functions import *


api = Blueprint('api', __name__, template_folder="templates")

##### Работа с БД Product #####
@api.route('/products/', methods=['GET']) 
def get_products():
    """Получает список всех продуктов.
    
    Возвращает:
        dict: JSON-ответ со списком продуктов.
    """
    products = Product.select()
    return jsonify({'products': [{'id': obj.id, 'name': obj.name, 'type': obj.type, 'calories': obj.calories, 'ingredients': obj.ingredients, 'allergic': obj.allergic} for obj in products]})


##### Работа с БД QR #####
@api.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    """Получает информацию о продукте по его ID.
    
    Аргументы:
        id (int): Идентификатор продукта.
    
    Возвращает:
        dict: JSON-ответ с информацией о продукте.
    """
    product = bd_get_product(id)
    return jsonify(product)

@api.route('/qr_products/<int:page>', methods=['GET'])
def get_qr_products_limit(page):
    """Получает список QR-продуктов постранично.
    
    Аргументы:
        page (int): Номер страницы.
    
    Возвращает:
        dict: JSON-ответ со списком QR-продуктов.
    """
    return jsonify(bd_get_qr_products(page))

@api.route('/product/<int:id>', methods=['DELETE'])
def product_delete(id):
    """Удаляет QR-продукт по ID.
    
    Аргументы:
        id (int): Идентификатор QR-продукта.
    
    Возвращает:
        dict: JSON-ответ с подтверждением удаления.
    """
    product = QR.get(QR.id == str(id))
    product.deleted = True
    product.deleted_date = datetime.now()
    product.save()
    return jsonify({'msg': 'deleted'})


##### Работа с БД ShoppingListHistory #####
@api.route('/shopping_list', methods=['GET'])
def gset_shopping_history():
    """Получает историю покупок.
    
    Возвращает:
        dict: JSON-ответ с историей покупок.
    """
    products = bd_get_shopping_history()
    return jsonify(products)

@api.route('/shopping_list/<int:id>', methods=['DELETE'])
def delete_shopping_history(id):
    """Удаляет запись из истории покупок.
    
    Аргументы:
        id (int): Идентификатор записи в истории.
    
    Возвращает:
        dict: JSON-ответ с подтверждением удаления.
    """
    history = ShoppingListHistory.get(ShoppingListHistory.id == str(id))
    history.deleted = True
    history.deleted_date = datetime.now()
    history.save()
    return jsonify({'msg': 'deleted'})


##### Работа с БД Storage #####
@api.route('/add_qr_product_storage', methods=['POST'])
def add_storage_product():
    """Добавляет QR-продукт в хранилище.
    
    Возвращает:
        dict: JSON-ответ с подтверждением добавления.
    """
    qr_id = request.json.get('qr_id')
    data = {'qr_product': qr_id}
    Storage.create(**data)
    return jsonify({'msg': 'added'})

@api.route('/expired_count', methods=['GET'])
def expired_count():
    """Получает количество просроченных продуктов.
    
    Возвращает:
        dict: JSON-ответ с количеством просроченных товаров.
    """
    count = bd_expired_count()
    return jsonify({'count': count})

@api.route('/soon_expire', methods=['GET'])
def soon_expire():
    """Получает количество товаров, срок годности которых истекает в ближайшие 7 дней.
    
    Возвращает:
        dict: JSON-ответ с количеством таких товаров.
    """
    count = Storage.select(Storage).join(QR, on=(Storage.qr_product == QR.id))\
        .where((QR.last_date > datetime.now()) & (QR.last_date < datetime.now() + timedelta(days=7)) & (Storage.deleted == 0)).count()
    return jsonify({'count': count})

@api.route('/storage/<int:page>', methods=['GET'])
def get_storage_products_limit(page):
    """Получает список товаров из хранилища постранично.
    
    Аргументы:
        page (int): Номер страницы.
    
    Возвращает:
        dict: JSON-ответ со списком товаров.
    """
    return jsonify(bd_get_storage_product(page))

@api.route('/storage/<int:id>', methods=['DELETE'])
def storage_delete(id):
    """Удаляет товар из хранилища по ID.
    
    Аргументы:
        id (int): Идентификатор товара в хранилище.
    
    Возвращает:
        dict: JSON-ответ с подтверждением удаления.
    """
    product = Storage.get(Storage.id == str(id))
    product.deleted = True
    product.deleted_date = datetime.now()
    product.save()
    return jsonify({'msg': 'deleted'})
