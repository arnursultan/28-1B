import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QVBoxLayout, QPushButton, QComboBox,
    QCheckBox, QRadioButton, QListWidget, QMessageBox
)

class WidgetDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Виджеты")
        self.setGeometry(200, 200, 500, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите имя")
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_input)

        self.description = QTextEdit()
        self.description.setPlaceholderText("Описание")
        layout.addWidget(QLabel("Описание:"))
        layout.addWidget(self.description)

        self.combo = QComboBox()
        self.combo.addItems(["Студент", "Преподаватель", "Разработчик"])
        layout.addWidget(QLabel("Роль:"))
        layout.addWidget(self.combo)

        self.check = QCheckBox("Согласен с условиями")
        layout.addWidget(self.check)

        self.radio1 = QRadioButton("Мужской")
        self.radio2 = QRadioButton("Женский")
        layout.addWidget(QLabel("Пол:"))
        layout.addWidget(self.radio1)
        layout.addWidget(self.radio2)

        self.list_widget = QListWidget()
        self.list_widget.addItems(["Python", "C++", "Java", "Go"])
        layout.addWidget(QLabel("Любимые языки:"))
        layout.addWidget(self.list_widget)

        self.submit_btn = QPushButton("Отправить")
        self.submit_btn.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def submit_data(self):
        name = self.name_input.text()
        desc = self.description.toPlainText()
        role = self.combo.currentText()
        agreed = self.check.isChecked()
        gender = "Мужской" if self.radio1.isChecked() else "Женский" if self.radio2.isChecked() else "Не выбран"
        selected_languages = [item.text() for item in self.list_widget.selectedItems()]

        if not name or not agreed:
            QMessageBox.warning(self, "Ошибка", "Введите имя и согласитесь с условиями!")
            return

        info = f"Имя: {name}\nРоль: {role}\nПол: {gender}\nОписание: {desc}\nЯзыки: {', '.join(selected_languages)}"
        QMessageBox.information(self, "Данные отправлены", info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = WidgetDemo()
    demo.show()
    sys.exit(app.exec())