from .db_connection import get_connection

def add_product(title, price):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO products (title, price) VALUES (?, ?)", (title, price))
        conn.commit()

def get_all_products():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, price FROM products")
        return cur.fetchall()

