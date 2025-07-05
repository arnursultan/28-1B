import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QLineEdit, QLabel, QMessageBox, QHBoxLayout, QFrame, QMainWindow
)
from PyQt6.QtCore import QPropertyAnimation, QRect, QEasingCurve, Qt, QTimer
from PyQt6.QtGui import QIcon, QPalette, QColor, QFont

DB_NAME = "LS8.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            description TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clients and Orders")
        self.setGeometry(100, 100, 600, 700)
        self.setWindowIcon(QIcon("icon.png"))

        self.setStyle()
        self.setup_ui()
        self.refresh_clients(animated=False)

    def setStyle(self):
        palette = self.palette()
        palette.setColor()