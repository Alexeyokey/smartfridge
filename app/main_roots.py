from flask import Blueprint, render_template

main = Blueprint('main', __name__, template_folder="templates")

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/qrscan', methods=['GET'])
def qrscan():
    return render_template('index.html')

@main.route('/qrprint', methods=['GET'])
def qrprint():
    return render_template('index.html')

@main.route('/filters', methods=['GET'])
def filters():
    return render_template('index.html')