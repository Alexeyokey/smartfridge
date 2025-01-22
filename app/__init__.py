from flask import Flask

# from app.bd import bd_session
# инициализация приложения, импортирование рутов и конфигов
def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    # bd_session.global_init('MYSQL_URL')

    from .main_roots import main
    from .api_roots import api
    
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    return app