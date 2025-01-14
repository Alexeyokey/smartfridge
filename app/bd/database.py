from peewee import *

db = SqliteDatabase('stores.db')
db.connect()
# class Basic(Model):
#     class Meta:
#         database = db # This model uses the "people.db" database.
        
class Store(Model):
    id = PrimaryKeyField()
    name = CharField(max_length=256)
    address = CharField(max_length=256)

    class Meta:
        database = db # This model uses the "people.db" database.

class Scaner(Model):
    id = PrimaryKeyField()
    store = ForeignKeyField(Store, to_field='id')
    class Meta:
        database = db

class Product(Model):
    id = PrimaryKeyField()
    price = IntegerField()
    discount_percent = IntegerField()
    name = CharField()
    type = CharField()
    ingredients = CharField()
    allergic = BooleanField()

    class Meta:
        database = db

class ShoppingListHistory(Model):
    id = PrimaryKeyField()
    product = ForeignKeyField(Product, to_field='id')
    scaner = ForeignKeyField(Scaner, to_field='id')
    
    class Meta:
        database = db

db.create_tables([Store, Scaner, Product, ShoppingListHistory])