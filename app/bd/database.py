from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
from peewee import *
db = MySQLDatabase('fridge', host='127.0.0.1', port=3306, user='root', password='')
  
# class Store(Model):
#     id = PrimaryKeyField() 
#     name = CharField(max_length=256)
#     address = CharField(max_length=256)

#     class Meta:
#         database = db # This model uses the "people.db" database.
# описывает магазинг с его именем и адресом

# class Scaner(Model):
#     id = PrimaryKeyField() 
#     store = ForeignKeyField(Store, to_field='id')
#     password = CharField()
#     class Meta:
#         database = db

#     def add_password(self):
#         return generate_password_hash
    
#     def check_password_hash(self):
#         return check_password_hash
# # таблциа каждого уникального холодильника, каждый холодильник имеет свой код доступа и привязку к магазину 


class Product(Model):
    id = PrimaryKeyField()
    name = CharField()
    type = CharField()
    ingredients = CharField()
    allergic = BooleanField()
    class Meta:
        database = db
    
class QR(Model):
    id = PrimaryKeyField()
    product = ForeignKeyField(Product, to_field='id')
    count = IntegerField()
    price = IntegerField()
    discount_percent = IntegerField()
    produced_date = DateTimeField()
    last_date = DateTimeField()
    class Meta:
        database = db
    
# Таблица единичного экземпляра продукта, содержащая всю информацию о его свойствах

class Fridge(Model):
    id = PrimaryKeyField() 
    product = ForeignKeyField(QR, to_field='id')
    # count = IntegerField()
    class Meta:
        database = db
    


class ShoppingListHistory(Model):
    id = PrimaryKeyField()
    product = ForeignKeyField(Product, to_field='id')
    quantity = IntegerField()
    # scaner = ForeignKeyField(Scaner, to_field='id')
    
    class Meta:
        database = db
# список всех покупок, совершенных через сканеры, каждая сущность прявязана к продукту и холодильнику


db.create_tables([Product, QR, Fridge, ShoppingListHistory])
sample_products = [
    {"name": "Chocolate Bar", "type": "Snack",
     "ingredients": "Cocoa, Sugar, Milk", "allergic": True},
    {"name": "Apple Juice", "type": "Drink",
     "ingredients": "Apple, Water, Sugar", "allergic": False},
    {"name": "Peanut Butter", "type": "Spread",
     "ingredients": "Peanuts, Salt, Oil", "allergic": True}
]

# Insert sample objects into the database
# print(sample_products)
# for product in sample_products:
#     Product.create(**product)

# print(datetime.now())
# for product in [1, 2, 3]:
#     QR.create(
#         product=product,
#         price=1000,  # Example price
#         count=product * 10,
#         discount_percent=10,  # Example discount percent
#         produced_date=datetime.now() - 2 * timedelta(days=product * 10),
#         last_date=datetime.now() - timedelta(days=product * 30),
#     )

# qr_product = QR.select().where(QR.id == '1').get()
# print(qr_product.product.name)