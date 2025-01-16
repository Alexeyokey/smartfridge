from config import SECRET_KEY
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='', port=3306)
conn.cursor().execute('CREATE DATABASE mydatabase')
conn.close()