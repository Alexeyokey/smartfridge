import qrcode
from app import PORT
import os

def get_qrcode(id):
    url = f'http://127.0.0.1:{PORT}/product/{id}' # создаем ссылку на продукт, ссылающую на json с информацией о продукте
    
    qr = qrcode.make(url) 
    path = os.path.join('app/static/qr_codes', f'qr_{id}.png') # создание пути и названия для qr code файла
    qr.save(path, 'PNG') # сохранение qr code в заданной директории
 

# def remove_qrcode(id):
