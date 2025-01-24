from flask import Flask
from flask_socketio import SocketIO
from .setting_param import PORT, COUNT_PAGE
from .forms import *
# from app.bd import bd_session
# инициализация приложения, импортирование рутов и конфигов
socketio = SocketIO(cors_allowed_origins="*")  # Разрешаем CORS для всех

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    socketio.init_app(app)
    print('1')
    # bd_session.global_init('MYSQL_URL')

    from .main_roots import main
    from .api_roots import api
    
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    return app