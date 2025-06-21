# Главные команды:
# 1. CREATE TABLE
# 2. INSERT INTO
# 3. SELECT
# 4. UPDATE
# 5. DELETE

import sqlite3
conn = sqlite3.connect("my_db.db")
cursor = conn.cursor()
print("✅ Успешное подключение к базе данных!")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    age INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price REAL NOT NULL
)
""")

conn.commit()
print("✅ Таблицы созданы.")

cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                ("Geeks", "geeks1@gmail.com", 7))

products = [
    ("Ноутбук", 45000.99),
    ("Клавиатура", 4990.99),
    ("Мышь", 3599.99)
]
cursor.executemany("INSERT INTO products (title, price) VALUES (?, ?)", products)
conn.commit()
print("✅ Данные добавлены.")

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print("\n Список пользователей:")
for u in users:
    print(f"{u[0]}. {u[1]} | {u[2]} | возраст: {u[3]}")

cursor.execute("SELECT * FROM products")
products = cursor.fetchall()
print("\n Список продуктов:")
for p in products:
    print(f"{p[0]}. {p[1]} - ${p[2]}")

conn.close()
print("\n Соединение  базой данных закрыта.")