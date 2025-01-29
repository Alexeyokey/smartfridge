import eventlet
eventlet.monkey_patch()
from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from app import PORT


app = create_app()


from app import socketio
import datetime

@socketio.on('connect')
def handle_connect():
    print("Клиент подключен!")

@socketio.on('disconnect')
def handle_disconnect():
    print("Клиент отключился!")

@socketio.on('notification')
def send_notification():
    # products
    """Функция для отправки уведомления"""
    count = requests.get(f'http://127.0.0.1:{PORT}/api/expired_count').json()
    now = datetime.datetime.now().strftime('%H:%M:%S')
    message = f"ИСПОРЧЕНО ПРОДУКТОВ: {count['count']} ПРОВЕДИТЕ РЕВИЗИЮ"
    # print(products)
    socketio.emit('notification', {'message': message})


scheduler = BackgroundScheduler()
scheduler.add_job(send_notification, 'interval', minutes=10)
scheduler.start()

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5001, allow_unsafe_werkzeug=True)