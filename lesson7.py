import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox, QListWidget
)

DB_NAME = "data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

class CRUDApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 CRUD Example")
        self.setGeometry(100, 100, 500, 400)

        self.layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.layout.addWidget(QLabel("Имя:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Email:"))
        self.layout.addWidget(self.email_input)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.update_btn = QPushButton("Изменить")
        self.delete_btn = QPushButton("Удалить")
        self.refresh_btn = QPushButton("Обновить список")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.refresh_btn)

        self.layout.addLayout(btn_layout)

        self.user_list = QListWidget()
        self.layout.addWidget(self.user_list)

        self.setLayout(self.layout)

        self.add_btn.clicked.connect(self.add_user)
        self.update_btn.clicked.connect(self.update_user)
        self.delete_btn.clicked.connect(self.delete_user)
        self.refresh_btn.clicked.connect(self.load_users)
        self.user_list.itemClicked.connect(self.load_selected_user)

        self.load_users()

    def db_query(self, query, params=(), fetch=False):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
        else:
            result = None
        conn.commit()
        conn.close()
        return result

    def load_users(self):
        self.user_list.clear()
        users = self.db_query("SELECT id, name, email FROM users", fetch=True)
        for user in users:
            item_text = f"{user[0]}: {user[1]} ({user[2]})"
            self.user_list.addItem(item_text)

    def add_user(self):
        name = self.name_input.text()
        email = self.email_input.text()
        if not name or not email:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        self.db_query("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        QMessageBox.information(self, "Успех", "Пользователь добавлен")
        self.load_users()
        self.name_input.clear()
        self.email_input.clear()

    def load_selected_user(self, item):
        parts = item.text().split(":")
        user_id = parts[0]
        user = self.db_query("SELECT name, email FROM users WHERE id = ?", (user_id,), fetch=True)
        if user:
            self.name_input.setText(user[0][0])
            self.email_input.setText(user[0][1])

    def update_user(self):
        selected_item = self.user_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для изменения")
            return
        parts = selected_item.text().split(":")
        user_id = parts[0]

        name = self.name_input.text()
        email = self.email_input.text()
        if not name or not email:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        self.db_query(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (name, email, user_id)
        )
        QMessageBox.information(self, "Успех", f"Пользователь {user_id} обновлен")
        self.load_users()

    def delete_user(self):
        selected_item = self.user_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для удаления")
            return
        parts = selected_item.text().split(":")
        user_id = parts[0]
        self.db_query("DELETE FROM users WHERE id = ?", (user_id,))
        QMessageBox.information(self, "Успех", f"Пользователь {user_id} удален")
        self.load_users()
        self.name_input.clear()
        self.email_input.clear()

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = CRUDApp()
    window.show()
    sys.exit(app.exec())