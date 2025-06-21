from .db_connection import  get_connection
import sqlite3

def add_user(name, email, age):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", (name, email, age))
            conn.commit()
            return True
    except sqlite3.IntegrityError as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        return False

def get_all_users():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, age FROM users")
        return cur.fetchall()

