from flask import jsonify
from datetime import datetime, timedelta
from app import COUNT_PAGE
from app.bd.database import Storage, ShoppingListHistory, QR, Product



def bd_get_storage_product(page):
    # print(Storage.qr_product.last_date)
    products = Storage.select(Storage).join(QR, on=(Storage.qr_product == QR.id)).where(Storage.id > (page - 1) * COUNT_PAGE).order_by(QR.last_date).limit(COUNT_PAGE)
    
    # select * from products WHERE id > (page - 1) * COUNT_PAGE LIMIT COUNT_PAGE
    expired_products = {}
    expire_soon = {}
    for obj in products:
          if not obj.deleted:
            expired_products[obj.id] = datetime.now() > obj.qr_product.last_date
            expire_soon[obj.id] = datetime.now() + timedelta(days=7) > obj.qr_product.last_date
    # print(expire_soon)

    return {'products': [{'id': obj.id, 'name': obj.qr_product.product.name, 'calories': obj.qr_product.product.calories, 'type': obj.qr_product.product.type, 
                                  'price': obj.qr_product.price, 'measurement': obj.qr_product.type_measurement, 'type_measurement': obj.qr_product.type_measurement, 'produced_date': obj.qr_product.produced_date, 'last_date': obj.qr_product.last_date, 
                                  'expired': expired_products[obj.id], 'soon': expire_soon[obj.id]} for obj in products if not obj.deleted]}

def bd_get_qr_products(page):
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
    return {'products': [{'id': obj.id, 'name': obj.product.name, 'type': obj.product.type, 'price': obj.price, 'measurement': obj.measurement, 'type_measurement': obj.type_measurement, 'produced_date': obj.produced_date, 'last_date': obj.last_date, 'expired': expired_products[obj.id]} for obj in products]}


##### Работа с БД ShoppingListHistory #####
# код для работы с таблицей ShoppingListHistorys
def bd_get_shopping_history():
    products = ShoppingListHistory.select()

    return {'products': [{'id': obj.id, 'name': obj.product.name, 'quantity': obj.quantity}  for obj in products if not obj.deleted]}


# код для работы с таблицей Storage
def bd_expired_count():
    count = Storage.select(Storage).join(QR, on=(Storage.qr_product == QR.id)).where((QR.last_date < datetime.now()) & (Storage.deleted == 0)).count()
    return {'count': count}