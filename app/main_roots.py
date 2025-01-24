from flask import Blueprint, render_template, request, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import Optional, DataRequired, NumberRange
import qrcode, io
import requests
from app import PORT
from app.bd.database import Product
from app.bd.database import QR

# from app.bd.database import Product
main = Blueprint('main', __name__, template_folder="templates")

class SearchForm(FlaskForm):
    query = StringField('SEARCH', validators=[Optional()] )
    submit = SubmitField(('ПОИСК'))

@main.route('/', methods=['GET', "POST"])
def index():
    form = SearchForm()
    table = requests.get(f'http://127.0.0.1:{PORT}/api/products/1').json()['products']
    # print(table)
    # if request.method == "GET":
    query = request.args.get('query', '').strip().lower()

        # Фильтрация таблицы по поисковому запросу
    if query:
        table = [row for row in table if query in row['name'].lower() or query in row['type'].lower()]
        # return render_template('index.html', table=table, form=form)
    

    return render_template('main.html', table=table, form=form)

@main.route('/generate_qr/<int:product_id>', methods=['GET', "POST"])
def generate_qr(product_id):
    url = f'http://127.0.0.1:{PORT}/product/{product_id}'
    qr = qrcode.make(url)
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='scripts/images/PNG')


@main.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
    product_json = requests.get(f'http://127.0.0.1:{PORT}/api/product/{product_id}')
    if product_json.status_code == 200:
        # print(product_json.json())
        return render_template('product.html', products=product_json.json()['products'])

class AddQRForm(FlaskForm):
    product = SelectField('Product', choices=[], coerce=int, validators=[DataRequired()])
    count = IntegerField('Count', validators=[DataRequired(), NumberRange(min=1)])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    discount_percent = IntegerField('Discount Percent', validators=[NumberRange(min=0, max=100)])
    produced_date = DateTimeField('Produced Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    last_date = DateTimeField('Last Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Add Product')

products = [(1, 'Product 1'), (2, 'Product 2'), (3, 'Product 3')]  # Заглушка


@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = AddQRForm()
    # Устанавливаем choices для SelectField из базы данных (или списка продуктов)
    form.product.choices = products
    
    # print(form.submit())
    # print(form.errors)
    if form.validate_on_submit() or request.method == "POST":
        # Сохранение данных из формы в базу данных
        data = {
            'product': form.product.data,
            'count': form.count.data,
            'price': form.price.data,
            'discount_percent': form.discount_percent.data,
            'produced_date': form.produced_date.data,
            'last_date': form.last_date.data
        }
        print(data)
        # QR.create(data[0])
        # Здесь добавьте логику сохранения в базу данных
        # print(f"Saving data: {data}")
        return "Product added successfully!"

    return render_template('add_product.html', form=form)
    
@main.route('/shopping_list/<int:page>', methods=['GET'])
def shopping_list(page):
    products = requests.get(f'/api/shopping_list/{page}')
    return render_template('shopping_list.html', product=product)


@main.route('/scan', methods=['GET'])
def scan():
    return render_template('qrscan.html')

@main.route('/base', methods=['GET'])
def base():
    return render_template('base.html')

# @main.route('/qrprint', methods=['GET'])
# def qrprint():
#     return render_template('main.html')

# @main.route('/filters', methods=['GET'])
# def filters():
#     return render_template('main.html')