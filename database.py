import sqlite3

def get_connection():
    return sqlite3.connect("people.db")

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_person(name, age):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO people (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

def get_all_people():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM people")
    people = cur.fetchall()
    conn.close()
    return people