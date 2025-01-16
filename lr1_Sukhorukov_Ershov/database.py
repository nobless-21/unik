import sqlite3

class Database:
    def __init__(self, db_name="bot_data.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.ensure_balance_column()

    def create_table(self):
        """Создание таблицы пользователей в базе данных"""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT
        )''')
        self.conn.commit()

    def ensure_balance_column(self):
        """Проверяем и добавляем колонку 'balance', если она отсутствует"""
        self.cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in self.cursor.fetchall()]
        if "balance" not in columns:
            self.cursor.execute("ALTER TABLE users ADD COLUMN balance INTEGER DEFAULT 0")
            self.conn.commit()

    def save_user(self, chat_id, username, first_name, last_name):
        """Сохранение пользователя в базу данных"""
        self.cursor.execute("""
            INSERT OR IGNORE INTO users (chat_id, username, first_name, last_name) 
            VALUES (?, ?, ?, ?)
        """, (chat_id, username, first_name, last_name))
        self.conn.commit()

    def get_user(self, chat_id):
        """Получение пользователя по chat_id"""
        self.cursor.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
        return self.cursor.fetchone()

    def update_balance(self, chat_id, amount):
        """Обновление баланса пользователя"""
        self.cursor.execute("""
            UPDATE users 
            SET balance = balance + ? 
            WHERE chat_id = ?
        """, (amount, chat_id))
        self.conn.commit()

    def get_balance(self, chat_id):
        """Получение баланса пользователя"""
        self.cursor.execute("SELECT balance FROM users WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def close(self):
        """Закрытие соединения с базой данных"""
        self.conn.close()
