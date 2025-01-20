from flask import Flask, render_template, jsonify, request, redirect, url_for
from threading import Thread
from bot import run_bot, send_admin_notification  # Импортируем функцию send_message из bot.py
from database import Database

app = Flask(__name__)
db = Database()


# Главная страница
@app.route('/')
def index():
    return render_template('index.html', message="This project was build by Sukhorukov, Ershov")


# Статус бота
@app.route('/status')
def status():
    return render_template('status.html', message="ТГ бот запущен")


# Получение всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    users = db.get_all_users()
    return render_template('users.html', users=users)

@app.route('/bets', methods=['GET'])
def get_bets():
    bets = db.cursor.execute("SELECT * FROM bets").fetchall()
    return render_template('bets.html', bets=bets)

# Добавление нового пользователя
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
    return redirect(url_for('get_users'))


# Обновление баланса пользователя
@app.route('/update_balance/<int:user_id>', methods=['POST'])
def update_balance(user_id):
    new_balance = request.form.get('new_balance')
    if new_balance:
        db.cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
        db.conn.commit()
        return redirect(url_for('get_users'))
    return redirect(url_for('get_users'))


# Удаление пользователя
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    db.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.conn.commit()
    return redirect(url_for('get_users'))


# Назначение роли администратора
@app.route('/set_admin/<int:user_id>', methods=['POST'])
def set_admin(user_id):
    # Назначаем роль администратора пользователю
    db.set_admin(user_id, is_admin=True)

    # Получаем chat_id пользователя из базы данных
    user = db.get_user(user_id)
    if user:
        chat_id = user[1]  # chat_id пользователя
        # Отправляем уведомление пользователю через бота
        send_admin_notification(chat_id)

    return redirect(url_for('get_users'))  # Перенаправляем на страницу пользователей


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
