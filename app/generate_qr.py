import qrcode
from app import PORT
import base64

import json
from app.bd.database import QR
import os

def get_qrcode(qr_code):
    id = qr_code.id
    data = {
        "id": qr_code.id,
        "name": qr_code.product.name,
        "type": qr_code.product.type,
        "produced": str(qr_code.produced_date),
        "last": str(qr_code.last_date),
        "measurement": qr_code.measurement,
        "type_measurement": qr_code.type_measurement,
        "calories": qr_code.product.calories,
    }
    qr = qrcode.make(json.dumps(data)) 
    path = os.path.join('app/static/qr_codes', f'qr_{id}.png') # создание пути и названия для qr code файла
    qr.save(path, 'PNG') # сохранение qr code в заданной директории
