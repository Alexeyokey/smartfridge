from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
from peewee import *
from .db_config import TABLE, HOST, PORT, USER, PASSWORD

db = SqliteDatabase('fridge.sqlite')
# db = MySQLDatabase(TABLE, host=HOST, port=PORT, user=USER, password=PASSWORD)


class Product(Model):
    id = PrimaryKeyField()
    name = CharField()
    type = CharField()
    calories = IntegerField()
    ingredients = CharField()
    allergic = BooleanField()
    class Meta:
        database = db
    
class QR(Model):
    id = PrimaryKeyField()
    product = ForeignKeyField(Product, to_field='id')
    count = IntegerField(default=1)
    measurement = IntegerField()
    type_measurement = CharField()
    price = IntegerField()
    discount_percent = IntegerField()
    produced_date = DateTimeField()
    last_date = DateTimeField()
    
    class Meta:
        database = db
    
# Таблица единичного экземпляра продукта, содержащая всю информацию о его свойствах

class Storage(Model):
    id = PrimaryKeyField() 
    qr_product = ForeignKeyField(QR, to_field='id')
    deleted = BooleanField(default=False)
    deleted_date = DateTimeField(null=True)
    class Meta:
        database = db
    

class ShoppingListHistory(Model):
    id = PrimaryKeyField()
    product = ForeignKeyField(Product, to_field='id')
    quantity = IntegerField()
    deleted = BooleanField(default=False)
    deleted_date = DateTimeField(null=True)
    class Meta:
        database = db
# список всех покупок, совершенных через сканеры, каждая сущность прявязана к продукту и холодильнику


db.create_tables([Product, QR, Storage, ShoppingListHistory])
