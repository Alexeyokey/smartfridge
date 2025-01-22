from flask import Blueprint, render_template, request, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional
import qrcode, io
import requests
# from app.bd.database import Product
main = Blueprint('main', __name__, template_folder="templates")

class SearchForm(FlaskForm):
    query = StringField("Поиск", validators=[Optional()])
    submit = SubmitField(('ПОИСК'))

@main.route('/', methods=['GET', "POST"])
def index():
    form = SearchForm()
    table = requests.get('http://127.0.0.1:5000/api/products/1').json()['products']
    print(table)
    # if request.method == "GET":
    query = request.args.get('query', '').strip().lower()

        # Фильтрация таблицы по поисковому запросу
    if query:
        table = [row for row in table if query in row['name'].lower()]
        # return render_template('index.html', table=table, form=form)
    

    return render_template('main.html', table=table, form=form)

@main.route('/generate_qr/<int:product_id>', methods=['GET', "POST"])
def generate_qr(product_id):
    url = f'https://127.0.0.1:5000/product/{product_id}'
    qr = qrcode.make(url)
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='scripts/images/PNG')


@main.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
    product_json = requests.get(f'http://127.0.0.1:5000/api/product/{product_id}')
    if product_json.status_code == 200:
        print(product_json.json())
        return render_template('product.html', products=product_json.json()['products'])
    
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