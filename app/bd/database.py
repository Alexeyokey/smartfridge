from werkzeug.security import generate_password_hash, check_password_hash

from peewee import *
db = MySQLDatabase('fridge', host='127.0.0.1', port=3306, user='root', password='')
class MyUser (Model):
   name=TextField()
   city=TextField(constraints=[SQL("DEFAULT 'Mumbai'")])
   age=IntegerField()
   class Meta:
      database=db
      db_table='MyUser'
db.connect()
# db.create_tables([MyUser])

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
    password = CharField()
    class Meta:
        database = db

    def add_password(self):
        return generate_password_hash
    
    def check_password_hash(self):
        return check_password_hash


class Product(Model):
    id = PrimaryKeyField()
    name = CharField()
    type = CharField()
    price = IntegerField()
    discount_percent = IntegerField()
    ingredients = CharField()
    allergic = BooleanField()
    # store = ForeignKeyField(Store, to_field='id')

    class Meta:
        database = db

class ShoppingListHistory(Model):
    id = PrimaryKeyField()
    product = ForeignKeyField(Product, to_field='id')
    scaner = ForeignKeyField(Scaner, to_field='id')
    
    class Meta:
        database = db


db.create_tables([Store, Scaner, Product, ShoppingListHistory, Ingredient])