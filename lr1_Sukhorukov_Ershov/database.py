import sqlite3

class Database:
    def __init__(self, db_name="bot_data.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)  # Указываем check_same_thread=False
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Создание таблицы пользователей в базе данных"""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            username TEXT,
            first_name TEXT,
            last_name TEXT
        )''')
        self.conn.commit()

    def save_user(self, chat_id, username, first_name, last_name):
        """Сохранение пользователя в базу данных"""
        self.cursor.execute("INSERT INTO users (chat_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
                            (chat_id, username, first_name, last_name))
        self.conn.commit()

    def get_user(self, chat_id):
        """Получение пользователя по chat_id"""
        self.cursor.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
        return self.cursor.fetchone()

    def close(self):
        """Закрытие соединения с базой данных"""
        self.conn.close()
