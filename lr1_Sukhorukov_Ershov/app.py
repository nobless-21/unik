from flask import Flask, render_template, jsonify, request
from threading import Thread
from bot import run_bot  # Импортируем функцию run_bot из bot.py
from database import Database

app = Flask(__name__)
db = Database()

# Главная страница
@app.route('/')
def index():
    return render_template('index.html', message="Привет, это Flask + Telegram Bot!")

# Пример API для получения статуса бота
@app.route('/status')
def status():
    return jsonify({"status": "running"})

# Получение всех пользователей из базы данных
@app.route('/users', methods=['GET'])
def get_users():
    users = db.cursor.execute("SELECT * FROM users").fetchall()
    return jsonify(users)

# Добавление пользователя в базу данных через Flask
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    chat_id = data.get('chat_id')
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    db.save_user(chat_id, username, first_name, last_name)
    return jsonify({"message": "Пользователь добавлен"})

# Запуск Flask-приложения
def start_flask():
    app.run(host='0.0.0.0', port=5000)

# Запуск бота и Flask в отдельных потоках
def main():
    thread1 = Thread(target=start_flask)
    thread2 = Thread(target=run_bot)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()
