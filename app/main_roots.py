from flask import Blueprint, render_template, request, url_for, redirect, flash
import requests
from datetime import datetime
from app import PORT
from app.bd.database import Product, ShoppingListHistory
from app.bd.database import QR, Storage
from .forms import addqrform
from .forms import searchform, addform, productquantityform, analytics
from .generate_qr import get_qrcode 
from .bd_functions import *

# Создание объекта Blueprint для маршрутов главной части приложения
main = Blueprint('main', __name__, template_folder="templates")

##### Основные страницы #####
# Главная страница с таблицей продуктов и поисковой формой
@main.route('/', methods=['GET', "POST"])
def index():
    """
    Отображает главную страницу с таблицей продуктов и поисковой формой.
    Поддерживает пагинацию и фильтрацию списка продуктов по запросу пользователя.
    """
    form = searchform.SearchForm()  
    try:
        page = int(request.args.get('page', 1)) 
    except ValueError:
        page = 1
    try:
        table = bd_get_storage_product(page)['products']
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        table = []
  
    query = request.args.get('query', '').strip().lower()  
    if query:
        table = [row for row in table if query in row['name'].lower() or query in row['type'].lower()]

    return render_template('main.html', table=table, form=form, page=page, query=query)  

# Страница с аналитикой продуктов
@main.route('/analytics', methods=['GET', 'POST'])
def analytic():
    """
    Отображает страницу аналитики, включая статистику по удаленным и испорченным продуктам.
    Фильтрует данные по заданным пользователем датам.
    """
    form = analytics.AnalyticsDates()  
    products_deleted = Storage.select(Storage).where(Storage.deleted == 1)
    products_spoiled = Storage.select(Storage).join(QR, on=(Storage.qr_product == QR.id)).where(QR.last_date < datetime.now())
    count_deleted = products_deleted.count()
    count_spoiled = products_spoiled.count()
    types_count = {}
    
    if form.validate_on_submit(): 
        start_date = form.start_date.data 
        end_date = form.end_date.data 
        products_deleted = Storage.select(Storage).where((Storage.deleted == 1) & (Storage.deleted_date > start_date) & (Storage.deleted_date < end_date))
        products_spoiled = Storage.select(Storage).join(QR, on=(Storage.qr_product == QR.id)).where((QR.last_date < datetime.now()) & (QR.last_date > start_date) & (QR.last_date < end_date))

    for obj in products_deleted:
        types_count.setdefault(obj.qr_product.product.type, [0, 0])[0] += 1
    for obj in products_spoiled:
        types_count.setdefault(obj.qr_product.product.type, [0, 0])[1] += 1
    
    products = {
        "products": [{'type': obj[0], 'count_deleted': obj[1][0], 'count_spoiled': obj[1][1]} for obj in types_count.items()]
    }
    counted = {'counted': {'deleted': count_deleted, 'spoiled': count_spoiled}}
    
    return render_template('analytics.html', form=form, products=products['products'], counted=counted['counted'])  

# Страница для отображения информации о продукте
@main.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
    """
    Отображает страницу с подробной информацией о продукте по его ID.
    """
    product = bd_get_product(product_id)
    if product:
        in_storage = Storage.get_or_none(Storage.qr_product == product['product']['id'])
        form = productquantityform.ProductOrder(product_id=product['product']['product_id'])  

        if in_storage:
            return render_template('product.html', product=product['product'], form=form, save=not in_storage, storage_id=in_storage.id)
        else:
            return render_template('product.html', product=product['product'], form=form, save=not in_storage)
    else:
        return "Ошибка: Продукт не найден", 404

# Добавление записи в историю покупок
@main.route('/product/<int:id>', methods=['POST'])
def add_shopping_history(id):
    """
    Добавляет запись о покупке продукта в историю покупок.
    """
    form = productquantityform.ProductOrder()
    if form.validate_on_submit(): 
        data = {
            'product': form.product_id.data,
            'quantity': form.quantity.data
        }
        ShoppingListHistory.create(**data)
        return redirect('/shopping_list')  
    else:
        return "Неверные данные", 403

# Базовая страница шаблона
@main.route('/base', methods=['GET'])
def base():
    """
    Отображает базовую страницу шаблона.
    """
    return render_template('base.html')

##### Добавление продуктов и QR кодов #####
# Страница для добавления нового продукта
@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    """
    Отображает форму добавления нового продукта в базу данных.
    Проверяет существование продукта перед добавлением.
    """
    form = addform.AddForm()  
    if form.validate_on_submit():  
        data = {
            'name': form.name.data.lower(),
            'type': form.type.data.lower(),
            'calories': form.calories.data,
            'ingredients': form.ingredients.data.lower(),
            'allergic': form.allergic.data,
        }
        if not Product.get_or_none(Product.name == form.name.data):
            Product.create(**data) 
            return redirect('/add_qr_product')  
        flash('Такой продукт уже есть в базе данных')
    return render_template('add_form.html', form=form)  

# Страница для добавления нового QR-кода
@main.route('/add_qr_product', methods=['GET', 'POST'])
def add_qr_product():
    """
    Отображает форму для добавления QR-кода к продукту.
    Генерирует QR-код при успешной валидации формы.
    """
    form = addqrform.AddQRForm()
    json_products = requests.get(f'http://127.0.0.1:{PORT}/api/products').json()  
    form.product.choices = [(i['id'], i['name']) for i in json_products['products']]
    
    if form.validate_on_submit(): 
        if form.last_date.data <= form.produced_date.data:
            flash('Неверные даты')
            return render_template('add_form.html', form=form)
        if form.type_measurement == 'количество':
            count = form.measurement
        data = form.data
        count = 1
        data['count'] = count
        qr_code = QR.create(**form.data)  
        get_qrcode(qr_code)  
        return render_template('qr_code.html', qr_id=qr_code.id, url_product=url_for('static', filename=f'qr_codes/qr_{qr_code.id}.png'))
    return render_template('add_form.html', form=form)  


@main.route('/shopping_list', methods=['GET'])
def shopping_list():
    products = requests.get(f'http://127.0.0.1:{PORT}/api/shopping_list').json()  # Получение списка покупок с API
    return render_template('shopping_list.html', products=products['products'])  # Отображение списка покупок

##### QR #####
# Страница для сканирования QR-кодов
@main.route('/scan', methods=['GET'])
def scan():
    return render_template('qrscan.html')  # Отображение страницы для сканирования QR-кода
