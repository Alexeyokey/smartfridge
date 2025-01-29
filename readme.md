Запуск проекта:
pip install -r requirements.txt

скачивание mysql;
**1. Запуск mysql

`mysql -u root -p`

**2. Создание пользователя**

**CREATE **USER 'kate'**@**'localhost' IDENTIFIED **BY 'password123'**;

**3. Назначение привилегий**

**GRANT** **ALL** PRIVILEGES **ON** example_db.* **TO** **'new_user'**@**'localhost'**;

**4. Применение изменений**

FLUSH PRIVILEGES;

**5. Проверка**

mysql -u new_user -p

**6. Создание датабазы

create database fridge;
