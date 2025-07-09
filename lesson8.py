import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QLineEdit, QLabel, QMessageBox, QHBoxLayout, QFrame
)
from PyQt6.QtCore import QPropertyAnimation, QRect, QEasingCurve, Qt, QTimer
from PyQt6.QtGui import QIcon, QPalette, QColor, QFont

DB_NAME = "example.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            description TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clients and Orders")
        self.setGeometry(100, 100, 500, 600)
        self.setWindowIcon(QIcon("icon.ico"))

        self.setStyle()
        self.setup_ui()
        self.refresh_clients(animated=False)

    def setStyle(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2e3440"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#d8dee9"))
        self.setPalette(palette)
        self.setFont(QFont("Arial", 10))

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText("New client name")
        self.layout.addWidget(self.client_input)

        self.add_client_btn = QPushButton("Add Client")
        self.add_client_btn.clicked.connect(self.add_client)
        self.layout.addWidget(self.add_client_btn)

        self.layout.addWidget(QLabel("Clients:"))
        self.client_list = QListWidget()
        self.client_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.client_list.itemClicked.connect(self.load_orders)
        self.layout.addWidget(self.client_list)

        self.add_separator()

        filter_layout = QHBoxLayout()
        self.order_input = QLineEdit()
        self.order_input.setPlaceholderText("New order description")
        filter_layout.addWidget(self.order_input)

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter orders")
        self.filter_input.textChanged.connect(self.apply_order_filter)
        filter_layout.addWidget(self.filter_input)

        self.layout.addLayout(filter_layout)

        self.add_order_btn = QPushButton("Add Order to Selected Client")
        self.add_order_btn.clicked.connect(self.add_order)
        self.layout.addWidget(self.add_order_btn)

        self.layout.addWidget(QLabel("Orders:"))
        self.order_list = QListWidget()
        self.layout.addWidget(self.order_list)

        self.setLayout(self.layout)

        self.animations = []

    def add_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(line)

    def animate_widget(self, widget):
        animation = QPropertyAnimation(widget, b"geometry")
        rect = widget.geometry()
        animation.setDuration(400)
        animation.setStartValue(QRect(rect.x(), rect.y(), rect.width(), 0))
        animation.setEndValue(rect)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()
        self.animations.append(animation)

    def animate_button(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        rect = button.geometry()
        animation.setDuration(400)
        animation.setStartValue(QRect(rect.x(), rect.y() + 50, rect.width(), rect.height()))
        animation.setEndValue(rect)
        animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        animation.start()
        self.animations.append(animation)

    def add_client(self):
        name = self.client_input.text().strip()
        if not name:
            self.show_toast("Client name cannot be empty.")
            return
        conn = sqlite3.connect(DB_NAME)
        conn.execute("INSERT INTO clients (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        self.client_input.clear()
        self.refresh_clients()
        self.show_toast(f"Client '{name}' added.")

    def refresh_clients(self, animated=True):
        self.client_list.clear()
        conn = sqlite3.connect(DB_NAME)
        clients = conn.execute("SELECT id, name FROM clients").fetchall()
        conn.close()
        for id_, name in clients:
            self.client_list.addItem(f"{id_}: {name}")
        if animated:
            self.animate_widget(self.client_list)
            self.animate_button(self.add_client_btn)

    def load_orders(self, item):
        self.highlight_selected_client(item)
        self.refresh_orders(int(item.text().split(":")[0]))

    def refresh_orders(self, client_id):
        self.current_client_id = client_id
        self.order_list.clear()
        conn = sqlite3.connect(DB_NAME)
        orders = conn.execute("SELECT description FROM orders WHERE client_id=?", (client_id,)).fetchall()
        conn.close()
        for desc, in orders:
            self.order_list.addItem(desc)
        self.apply_order_filter()
        self.animate_widget(self.order_list)
        self.animate_button(self.add_order_btn)

    def add_order(self):
        selected = self.client_list.currentItem()
        if not selected:
            self.show_toast("Select a client first.")
            return
        description = self.order_input.text().strip()
        if not description:
            self.show_toast("Order description cannot be empty.")
            return
        client_id = int(selected.text().split(":")[0])
        conn = sqlite3.connect(DB_NAME)
        conn.execute("INSERT INTO orders (client_id, description) VALUES (?, ?)", (client_id, description))
        conn.commit()
        conn.close()
        self.order_input.clear()
        self.refresh_orders(client_id)
        self.show_toast(f"Order added to client {client_id}.")

    def apply_order_filter(self):
        keyword = self.filter_input.text().lower()
        for i in range(self.order_list.count()):
            item = self.order_list.item(i)
            item.setHidden(keyword not in item.text().lower())

    def highlight_selected_client(self, item):
        for i in range(self.client_list.count()):
            list_item = self.client_list.item(i)
            list_item.setBackground(QColor("#2e3440"))
        item.setBackground(QColor("#4c566a"))

    def show_toast(self, message):
        toast = QLabel(message, self)
        toast.setStyleSheet("background-color: #88c0d0; color: #2e3440; padding: 5px; border-radius: 5px;")
        toast.move(10, self.height() - 40)
        toast.show()
        QTimer.singleShot(2000, toast.deleteLater)

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())