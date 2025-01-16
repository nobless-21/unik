import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('bot_data.db')
cursor = conn.cursor()

# Запрос для просмотра всех записей в таблице
cursor.execute("SELECT * FROM bets")
rows = cursor.fetchall()

# Вывод результатов
for row in rows:
    print(row)

# Закрытие соединения
conn.close()