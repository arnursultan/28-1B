import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QTextEdit
)
from database import init_db, add_person, get_all_people

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD - Добавление и Получение")
        self.setGeometry(100, 100, 400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Возраст")

        self.add_button = QPushButton("Добавить человека")
        self.add_button.clicked.connect(self.handle_add)

        self.show_button = QPushButton("Показать всех")
        self.show_button.clicked.connect(self.handle_show)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)

        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Возраст:"))
        layout.addWidget(self.age_input)

        layout.addWidget(self.add_button)
        layout.addWidget(self.show_button)
        layout.addWidget(self.output_area)

        self.setLayout(layout)

    def handle_add(self):
        name = self.name_input.text()
        age = self.age_input.text()

        if name and age.isdigit():
            add_person(name, int(age))
            self.name_input.clear()
            self.age_input.clear()
            self.output_area.setText("Человек добавлен!")
        else:
            self.output_area.setText("Ошибка: введите имя и возраст (число)")

    def handle_show(self):
        people = get_all_people()
        result = ""
        for person in people:
            result += f"{person[0]}: {person[1]}, {person[2]} лет\n"
        self.output_area.setText(result)

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())