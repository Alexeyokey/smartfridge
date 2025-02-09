# Видео-демонстрация проекта
```https://rutube.ru/video/private/5259c214f17612b6b6e11642eda14a5e/?p=W8mS55NqKvbi8GE-UfyAVA```


# Установка проекта:
# Установка Node.js на Windows и macOS

## Установка на Windows
1. Перейдите на официальный сайт [Node.js](https://nodejs.org/).
2. Скачайте последний LTS-установщик для Windows.
3. Запустите установочный файл и следуйте инструкциям мастера установки.
4. Убедитесь, что установлены **Node.js** и **npm**, выполнив в командной строке:
   ```sh
   node -v
   npm -v
   ```

## Установка на macOS
### Установка через установщик:
1. Перейдите на официальный сайт [Node.js](https://nodejs.org/).
2. Скачайте последний LTS-установщик для macOS.
3. Запустите установочный файл и следуйте инструкциям.

### Установка через Homebrew:
1. Убедитесь, что Homebrew установлен:
   ```sh
   brew -v
   ```
2. Установите Node.js через Homebrew:
   ```sh
   brew install node
   ```
3. Проверьте установку:
   ```sh
   node -v
   npm -v
   ```
---

# Установка Tailwind CSS и билд стилей

1. Установите Tailwind CSS и других необходимых библиотек:
   ```sh
   npm i
   ```
2. Билд стилей:
   ```sh
   npm run build 
    ```

# Запуск бекенда
1. Создайте виртуальное окружение:
# Запуск бекенда
1. Создайте виртуальное окружение:
 • Linux/macOS:
 ```sh
 python3 -m venv venv
 ```
 • Windows:
 ```sh
 python -m venv venv
```

2. Активируйте виртуальное окружение:
 • Linux/macOS:
 ```sh
 source venv/bin/activate
 ```
 • Windows:
 ```sh
 venv\Scripts\activate
```

3. Обновите менеджер пакетов pip:
```sh
 pip install --upgrade pip
```
4. Скачивание библиотек
```sh
 pip install -r requirements.txt
```
5. Запуск веб аппа:
 • Linux/macOS:
 ```sh
 python3 run.py
 ```
 • Windows:
 ```sh
 python run.py
```
### Готово! перейдите по ссылке: http://127.0.0.1:5001
