from flask import Blueprint, render_template, request, url_for, redirect
import requests
from app import PORT
from app.bd.database import Product, ShoppingListHistory
from app.bd.database import QR
from .forms import addqrform
from .forms import searchform, addform, productquantityform
from .generate_qr import get_qrcode 

# Создание объекта Blueprint для маршрутов главной части приложения
main = Blueprint('main', __name__, template_folder="templates")

##### Основные страницы #####
# Главная страница с таблицей продуктов и поисковой формой
@main.route('/', methods=['GET', "POST"])
def index():
    form = searchform.SearchForm()  
    page = request.args.get('page', 1) 
    url = f'http://127.0.0.1:{PORT}/api/storage/{page}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                table = response.json()['products'] 
            except requests.exceptions.JSONDecodeError:
                print("Ошибка: Получен не-JSON ответ")
                table = []
        else:
            print(f"Ошибка: API вернул статус {response.status_code}")
            table = []
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        table = []
  
    query = request.args.get('query', '').strip().lower()  

    if query:
        table = [row for row in table if query in row['name'].lower() or query in row['type'].lower()]

    return render_template('main.html', table=table, form=form)  


# Страница для отображения информации о продукте
@main.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
    product_json = requests.get(f'http://127.0.0.1:{PORT}/api/product/{product_id}')
    print(product_json)
    if product_json.status_code == 200:
        form = productquantityform.Quantity()   
        return render_template('product.html', product=product_json.json()['product'], form=form)
    else:
        return "Ошибка: Продукт не найден", 404


@main.route('/product/<int:id>', methods=['POST'])
def add_shopping_history(id):
    form = productquantityform.Quantity()
    if form.validate_on_submit(): 
        data = {
                'product': id,
                'quantity': form.quantity.data
            }

        ShoppingListHistory.create(**data)
        return redirect('/shopping_list')  
    else:
        return "Неверные данные", 403
    

# Базовая страница шаблона
@main.route('/base', methods=['GET'])
def base():
    return render_template('base.html')  # Отображение базового шаблона

  
##### Добавление продуктов и QR кодов #####
# Страница для добавления нового продукта
@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    types = ['Snack', 'healthy'] # Список типов продуктов для выбора ЗАГЛУШКА!!!!!!!!!!!!!!
    form = addform.AddForm()  
    form.type.choices = types  
    if form.validate_on_submit():  
        data = {
            'name': form.name.data,
            'type': form.type.data,
            'calories': form.calories.data,
            'ingredients': form.ingredients.data,
            'allergic': form.allergic.data,
        }
        Product.create(**data) 
        return redirect('/add_qr_product')  

        

    return render_template('add_product.html', form=form)  

# Страница для добавления нового QR
@main.route('/add_qr_product', methods=['GET', 'POST'])
def add_qr_product():
    form = addqrform.AddQRForm()
    json_products = requests.get(f'http://127.0.0.1:{PORT}/api/products').json()  
    products = []
    for i in json_products['products']:
        products.append((i['id'], i['name']))
    form.product.choices = products 
    if form.validate_on_submit(): 
        if form.last_date.data <= form.produced_date.data:
            return "Ошибка: Дата истечения срока годности не может быть раньше даты производства", 400
        data = {
            'product': form.product.data,
            'count': form.count.data,
            'price': form.price.data,
            'discount_percent': form.discount_percent.data,
            'produced_date': form.produced_date.data,
            'last_date': form.last_date.data
        }
        # print(form.produced_date.data)
        qr_code = QR.create(**data)  # Создание нового QR-кода для продукта)
        # get_qrcode(qr_code.id)  # Генерация QR-кода
        product = requests.get(f'http://127.0.0.1:{PORT}/api/product/{qr_code.id}').json()  # Получение данных о продукте
        return render_template('qr_code.html', qr_id=qr_code.id, url_product=url_for('static', filename=f'qr_codes/qr_{qr_code.id}.png'))  # Отображение страницы с QR-кодом

    return render_template('add_qr_product.html', form=form)  # Отображение формы добавления продукта с QR-кодом

##### Списки #####
# Страница списка покупок с пагинацией
@main.route('/shopping_list', methods=['GET'])
def shopping_list():
    products = requests.get(f'http://127.0.0.1:{PORT}/api/shopping_list').json()  # Получение списка покупок с API
    return render_template('shopping_list.html', products=products['products'])  # Отображение списка покупок

##### QR #####
# Страница для сканирования QR-кодов
@main.route('/scan', methods=['GET'])
def scan():
    return render_template('qrscan.html')  # Отображение страницы для сканирования QR-кода

# Страница для генерации QR-кода для продукта
# @main.route('/generate_qr', methods=['GET', 'POST'])
# def generate_qr(product_id):
#     get_qrcode(product_id)  # Генерация QR-кода для продукта
#     product = requests.get(f'http://127.0.0.1:{PORT}/product/{product_id}').json()  # Получение данных о продукте по ID
#     return render_template('qr_code.html', product=product, product_id=product_id, url_product=url_for('static', filename=f'qr_codes/qr_{product_id}.png'))  # Отображение страницы с QR-кодом
