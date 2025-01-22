from werkzeug.security import generate_password_hash, check_password_hash

from peewee import *
db = MySQLDatabase('fridge', host='127.0.0.1', port=3306, user='root', password='')
  
class Store(Model):
    id = PrimaryKeyField() 
    name = CharField(max_length=256)
    address = CharField(max_length=256)

    class Meta:
        database = db # This model uses the "people.db" database.
# описывает магазинг с его именем и адресом

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
# таблциа каждого уникального холодильника, каждый холодильник имеет свой код доступа и привязку к магазину 



class Product(Model):
    id = PrimaryKeyField()
    name = CharField()
    type = CharField()
    price = IntegerField()
    discount_percent = IntegerField()
    ingredients = CharField()
    allergic = BooleanField()
    produced_date = DateTimeField()
    last_date = DateTimeField()
    # store = ForeignKeyField(Store, to_field='id')

    class Meta:
        database = db
# Таблица единичного экземпляра продукта, содержащая всю информацию о его свойствах

class ShoppingListHistory(Model):
    id = PrimaryKeyField()
    product = ForeignKeyField(Product, to_field='id')
    scaner = ForeignKeyField(Scaner, to_field='id')
    
    class Meta:
        database = db
# список всех покупок, совершенных через сканеры, каждая сущность прявязана к продукту и холодильнику


db.create_tables([Store, Scaner, Product, ShoppingListHistory])
sample_products = [
    {"name": "Chocolate Bar", "type": "Snack", "price": 200, "discount_percent": 10,
     "ingredients": "Cocoa, Sugar, Milk", "allergic": True, "produced_date": "2025-01-01 10:00:00", "last_date": "2025-06-01 10:00:00"},
    {"name": "Apple Juice", "type": "Drink", "price": 150, "discount_percent": 5,
     "ingredients": "Apple, Water, Sugar", "allergic": False, "produced_date": "2025-01-10 10:00:00", "last_date": "2025-03-10 10:00:00"},
    {"name": "Peanut Butter", "type": "Spread", "price": 300, "discount_percent": 15,
     "ingredients": "Peanuts, Salt, Oil", "allergic": True, "produced_date": "2025-01-15 10:00:00", "last_date": "2025-07-15 10:00:00"}
]

# Insert sample objects into the database
# print(sample_products))
for product in sample_products:
    Product.create(**product)
# for obj in Product.select():
#     print(obj.name)
    # print(i)
    # select * from products WHERE id > (page - 1) * COUNT_PAGE LIMIT COUNT_PAGE
# print(products, then)