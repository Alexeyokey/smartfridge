from flask import Blueprint, render_template, request, url_for
import requests
from app import PORT
from app.bd.database import Product
from app.bd.database import QR
from .forms import addqrform
from .forms import searchform, addform
from .generate_qr import get_qrcode 

# Создание объекта Blueprint для маршрутов главной части приложения
main = Blueprint('main', __name__, template_folder="templates")

# Главная страница с таблицей продуктов и поисковой формой
@main.route('/', methods=['GET', "POST"])
def index():
    form = searchform.SearchForm()  # Инициализация формы поиска
    page = request.args.get('page', 1)  # Получение текущей страницы
    url = f'http://127.0.0.1:{PORT}/api/qr_products/{page}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                table = response.json()['products']  # Проверка на валидный JSON
            except requests.exceptions.JSONDecodeError:
                print("Ошибка: Получен не-JSON ответ")
                table = []
        else:
            print(f"Ошибка: API вернул статус {response.status_code}")
            table = []
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        table = []
  
    query = request.args.get('query', '').strip().lower()  # Получение поискового запроса

    # Фильтрация таблицы по поисковому запросу
    if query:
        table = [row for row in table if query in row['name'].lower() or query in row['type'].lower()]

    return render_template('main.html', table=table, form=form)  # Отображение таблицы с продуктами

# Страница для генерации QR-кода для продукта
# @main.route('/generate_qr', methods=['GET', 'POST'])
# def generate_qr(product_id):
#     get_qrcode(product_id)  # Генерация QR-кода для продукта
#     product = requests.get(f'http://127.0.0.1:{PORT}/product/{product_id}').json()  # Получение данных о продукте по ID
#     return render_template('qr_code.html', product=product, product_id=product_id, url_product=url_for('static', filename=f'qr_codes/qr_{product_id}.png'))  # Отображение страницы с QR-кодом

# Страница для отображения информации о продукте
@main.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
    product_json = requests.get(f'http://127.0.0.1:{PORT}/api/product/{product_id}')
    if product_json.status_code == 200:
        return render_template('product.html', products=product_json.json()['products'])
    else:
        return "Ошибка: Продукт не найден", 404
  

# Страница для добавления нового продукта
@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    types = ['Snack', 'healthy'] # Список типов продуктов для выбора ЗАГЛУШКА!!!!!!!!!!!!!!
    form = addform.AddForm()  # Инициализация формы добавления продукта
    form.type.choices = types  # Установка вариантов выбора для поля типа продукта
    if form.validate_on_submit():  # Если форма успешно прошла валидацию
        # Сохранение данных из формы в базу данных
        data = {
            'name': form.name.data,
            'type': form.type.data,
            'ingredients': form.ingredients.data,
            'allergic': form.allergic.data,
        }
        Product.create(**data)  # Создание нового продукта в базе данных
        return "Product added successfully!"  # Сообщение об успешном добавлении

    return render_template('add_product.html', form=form)  # Отображение формы добавления продукта

# Страница для добавления продукта с QR-кодом
@main.route('/add_qr_product', methods=['GET', 'POST'])
def add_qr_product():
    form = addqrform.AddQRForm()  # Инициализация формы добавления продукта с QR-кодом
    json_products = requests.get(f'http://127.0.0.1:{PORT}/api/products').json()  # Получение списка продуктов с API
    products = []
    k = 0
    # Формирование списка кортежей (ID, название продукта) для поля выбора в форме
    for i in json_products['products']:
        k += 1
        products.append((k, i['name']))
    form.product.choices = products  # Установка вариантов выбора для поля продукта
    if form.validate_on_submit():  # Если форма успешно прошла валидацию
        # Сохранение данных из формы в базу данных
        data = {
            'product': form.product.data,
            'count': form.count.data,
            'calories': form.calories.data,
            'price': form.price.data,
            'discount_percent': form.discount_percent.data,
            'produced_date': form.produced_date.data,
            'last_date': form.last_date.data
        }
        # print(form.produced_date.data)
        qr_code = QR.create(**data)  # Создание нового QR-кода для продукта)
        get_qrcode(qr_code.id)  # Генерация QR-кода
        product = requests.get(f'http://127.0.0.1:{PORT}/api/product/{qr_code.id}').json()  # Получение данных о продукте
        return render_template('qr_code.html', qr_id=qr_code.id, url_product=url_for('static', filename=f'qr_codes/qr_{qr_code.id}.png'))  # Отображение страницы с QR-кодом

    return render_template('add_qr_product.html', form=form)  # Отображение формы добавления продукта с QR-кодом

# Страница списка покупок с пагинацией
@main.route('/shopping_list/<int:page>', methods=['GET'])
def shopping_list(page):
    products = requests.get(f'/api/shopping_list/{page}')  # Получение списка покупок с API
    return render_template('shopping_list.html', product=products)  # Отображение списка покупок

# Страница для сканирования QR-кодов
@main.route('/scan', methods=['GET'])
def scan():
    return render_template('qrscan.html')  # Отображение страницы для сканирования QR-кода

# Базовая страница шаблона
@main.route('/base', methods=['GET'])
def base():
    return render_template('base.html')  # Отображение базового шаблона
