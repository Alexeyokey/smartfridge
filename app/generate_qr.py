import qrcode, io
import requests
from app import PORT
import os

def get_qrcode(id):
    # print(os.path)
    url = f'http://127.0.0.1:{PORT}/product/{id}'
    
    qr = qrcode.make(url)
    # img_io = io.BytesIO()
    # print(os.path)
    img_io = os.path.join('app/static/qr_codes', f'qr_{id}.png')
    qr.save(img_io, 'PNG')
    

get_qrcode(1)