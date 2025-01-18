from flask import Flask, render_template, jsonify, request, redirect, url_for
from threading import Thread
from bot import run_bot  # Импортируем функцию run_bot из bot.py
from database import Database

app = Flask(__name__)
db = Database()

# Главная страница
@app.route('/')
def index():
    # Получение всех пользователей из базы данных
    users = db.cursor.execute("SELECT * FROM users").fetchall()
    # Получение всех ставок из таблицы bets
    bets = db.cursor.execute("SELECT * FROM bets").fetchall()
    return render_template('index.html', users=users, bets=bets, message="This project was build by Sukhorukov, Ershov")

# Пример API для получения статуса бота
@app.route('/status')
def status():
    return render_template('status.html', message="ТГ бот запущен")

# Получение всех пользователей из базы данных
@app.route('/users', methods=['GET'])
def get_users():
    users = db.cursor.execute("SELECT * FROM users").fetchall()
    return render_template('users.html', users=users)

# Получение всех ставок из базы данных
@app.route('/bets', methods=['GET'])
def get_bets():
    bets = db.cursor.execute("SELECT * FROM bets").fetchall()
    return render_template('bets.html', bets=bets)

# Добавление пользователя в базу данных через Flask
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.form
    chat_id = data.get('chat_id')
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if chat_id and username:
        db.save_user(chat_id, username, first_name, last_name)
        return redirect(url_for('get_users'))
    return redirect(url_for('get_users'))  # Перенаправляем обратно, если данные неверные

# Обновление баланса пользователя
@app.route('/update_balance/<int:user_id>', methods=['POST'])
def update_balance(user_id):
    new_balance = request.form.get('new_balance')
    if new_balance:
        db.cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
        db.conn.commit()
        return redirect(url_for('get_users'))  # После обновления баланса перенаправляем обратно на страницу пользователей
    return redirect(url_for('get_users'))  # В случае ошибки также возвращаемся на страницу пользователей

# Удаление пользователя
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    db.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.conn.commit()
    return redirect(url_for('get_users'))  # После удаления перенаправляем на страницу пользователей

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
