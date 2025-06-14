# QApplication - главный объект приложения, обрабатывает события.
# QWidget - базовый виджет(окно)
# QLabel, QPushButton, QLineEdit и др. - стандартные виджеты

#1
# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Привет, PyQt6!")
#         self.setGeometry(400, 800, 300, 200)
#
#         self.label = QLabel("Добро пожаловать в PyQt6!",self)
#         self.label.move(50, 80)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

#2
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Декомпозиция в PyQt6")
        self.setGeometry(100, 100, 400, 300)

        self.create_widgets()

    def create_widgets(self):
        self.label = QLabel("Привет, мир!",self)
        self.label.move(150, 100)

        self.button = QPushButton("Нажми меня",self)
        self.button.move(150, 150)
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        self.label.setText("Кнопка нажата!")
        self.label.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())