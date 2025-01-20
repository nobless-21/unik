import sqlite3

class Database:
    def __init__(self, db_name="bot_data.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.ensure_balance_column()
        self.ensure_is_admin_column()  # Добавляем проверку на наличие столбца is_admin

    def create_table(self):
        """Создание таблицы пользователей в базе данных"""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            balance INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0  -- Добавляем поле is_admin
        )''')
        self.conn.commit()

    def ensure_balance_column(self):
        """Проверяем и добавляем колонку 'balance', если она отсутствует"""
        self.cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in self.cursor.fetchall()]
        if "balance" not in columns:
            self.cursor.execute("ALTER TABLE users ADD COLUMN balance INTEGER DEFAULT 0")
            self.conn.commit()

    def ensure_is_admin_column(self):
        """Проверяем и добавляем колонку 'is_admin', если она отсутствует"""
        self.cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in self.cursor.fetchall()]
        if "is_admin" not in columns:
            self.cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
            self.conn.commit()

    def ensure_is_admin_column(self):
        """Проверяем и добавляем колонку 'is_admin', если она отсутствует"""
        self.cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in self.cursor.fetchall()]
        if "is_admin" not in columns:
            self.cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
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
        """Обновление баланса пользователя (добавление суммы)"""
        self.cursor.execute("""
            UPDATE users 
            SET balance = balance + ? 
            WHERE chat_id = ? 
        """, (amount, chat_id))
        self.conn.commit()

    def set_balance(self, chat_id, balance):
        """Устанавливаем новый баланс для пользователя"""
        self.cursor.execute("""
            UPDATE users 
            SET balance = ? 
            WHERE chat_id = ?
        """, (balance, chat_id))
        self.conn.commit()

    def get_balance(self, chat_id):
        """Получение баланса пользователя"""
        self.cursor.execute("SELECT balance FROM users WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_all_users(self):
        """Получение списка всех пользователей"""
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def get_all_bets(self):
        # Assuming you are using SQLite or any other DB
        # Replace with actual logic to fetch bets
        self.cursor.execute("SELECT * FROM bets")  # Modify the SQL query as per your schema
        return self.cursor.fetchall()

    def close(self):
        """Закрытие соединения с базой данных"""
        self.conn.close()

    def save_bet(self, chat_id, amount, coefficient, result):
        """Сохранение ставки в базу данных"""
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS bets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                amount INTEGER,
                coefficient REAL,
                result TEXT
            ) 
        ''')
        self.cursor.execute(
            "INSERT INTO bets (chat_id, amount, coefficient, result) VALUES (?, ?, ?, ?)",
            (chat_id, amount, coefficient, result)
        )
        self.conn.commit()

    def set_admin(self, user_id, is_admin=True):
        """Назначение пользователя администратором"""
        self.cursor.execute("UPDATE users SET is_admin = ? WHERE id = ?", (1 if is_admin else 0, user_id))
        self.conn.commit()

    def is_admin(self, chat_id):
        """Проверка, является ли пользователь администратором"""
        self.cursor.execute("SELECT is_admin FROM users WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        return result[0] == 1 if result else False

