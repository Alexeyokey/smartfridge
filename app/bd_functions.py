from flask import jsonify
from datetime import datetime, timedelta
from app import COUNT_PAGE
from app.bd.database import Storage, ShoppingListHistory, QR, Product


def bd_get_storage_product(page):
    """Извлекает список продуктов из bd, разбитый на страницы.
    
    Аргументы:
        page (int): Номер страницы для выборки товаров.
        
    Возвращает:
        dict: JSON-ответ, содержащий список продуктов с подробной информацией,
              включая статус истечения срока годности.
    """
    products = Storage.select(Storage).join(QR, on=(Storage.qr_product == QR.id))\
        .where(Storage.id > (page - 1) * COUNT_PAGE)\
        .order_by(QR.last_date).limit(COUNT_PAGE)
    
    expired_products = {}  # Словарь для хранения информации о просроченных продуктах
    expire_soon = {}  # Словарь для продуктов, срок годности которых скоро истечёт
    
    for obj in products:
        if not obj.deleted:
            expired_products[obj.id] = datetime.now() > obj.qr_product.last_date
            expire_soon[obj.id] = datetime.now() + timedelta(days=7) > obj.qr_product.last_date
    
    return {
        'products': [
            {
                'id': obj.id,
                'qr_id': obj.qr_product.id,
                'name': obj.qr_product.product.name,
                'calories': obj.qr_product.product.calories,
                'type': obj.qr_product.product.type,
                'count': obj.qr_product.count,
                'price': obj.qr_product.price,
                'measurement': obj.qr_product.type_measurement,
                'type_measurement': obj.qr_product.type_measurement,
                'produced_date': obj.qr_product.produced_date,
                'last_date': obj.qr_product.last_date,
                'expired': expired_products[obj.id],
                'soon': expire_soon[obj.id]
            }
            for obj in products if not obj.deleted
        ]
    }


def bd_get_qr_products(page):
    """Извлекает список QR-продуктов, разбитый на страницы.
    
    Аргументы:
        page (int): Номер страницы для выборки товаров.
        
    Возвращает:
        dict: JSON-ответ, содержащий список QR-продуктов с подробной информацией,
              включая статус истечения срока годности.
    """
    products = QR.select().where(QR.id > (page - 1) * COUNT_PAGE).order_by(QR.last_date).limit(COUNT_PAGE)
    expired_products = {obj.id: datetime.now() > obj.last_date for obj in products}  # Проверка на просроченность
    
    return {
        'products': [
            {
                'id': obj.id,
                'count': obj.count,
                'name': obj.product.name,
                'type': obj.product.type,
                'price': obj.price,
                'measurement': obj.measurement,
                'type_measurement': obj.type_measurement,
                'produced_date': obj.produced_date,
                'last_date': obj.last_date,
                'expired': expired_products[obj.id]
            }
            for obj in products
        ]
    }


def bd_get_product(id):
    """Получает информацию о конкретном продукте по его ID.
    
    Аргументы:
        id (int): Идентификатор продукта.
        
    Возвращает:
        dict: JSON-ответ с информацией о продукте.
    """
    obj = QR.get(QR.id == str(id))
    return {
        'product': {
            'id': obj.id,
            'count': obj.count,
            'name': obj.product.name,
            'type': obj.product.type,
            'price': obj.price,
            'product_id': obj.product.id,
            'measurement': obj.measurement,
            'type_measurement': obj.type_measurement,
            'produced_date': obj.produced_date,
            'last_date': obj.last_date,
            'allergic': obj.product.allergic
        }
    }


##### Работа с БД ShoppingListHistory #####
def bd_get_shopping_history():
    """Извлекает историю покупок.
    
    Возвращает:
        dict: JSON-ответ, содержащий список купленных товаров.
    """
    products = ShoppingListHistory.select()
    return {
        'products': [
            {'id': obj.id, 'name': obj.product.name, 'quantity': obj.quantity}
            for obj in products if not obj.deleted
        ]
    }


##### Работа с БД Storage #####
def bd_expired_count():
    """Подсчитывает количество просроченных продуктов и продуктов, срок годности которых скоро истечёт.
    
    Возвращает:
        dict: JSON-ответ с количеством просроченных продуктов и продуктов, срок годности которых истекает в ближайшие 7 дней.
    """
    soon_expire = Storage.select(Storage).join(QR, on=(Storage.qr_product == QR.id))\
        .where((QR.last_date > datetime.now()) & (QR.last_date < datetime.now() + timedelta(days=7)) & (Storage.deleted == 0)).count()
    expired = Storage.select(Storage).join(QR, on=(Storage.qr_product == QR.id))\
        .where((QR.last_date < datetime.now()) & (Storage.deleted == 0)).count()
    
    return {'count': expired, 'soon_count': soon_expire}
