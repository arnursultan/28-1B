import sys
import socket
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel

HOST = '127.0.0.1'
PORT = 65432

class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyQt6 Клиент')
        self.resize(400, 200)

        layout = QVBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText('Введите сообщение')
        layout.addWidget(self.input)

        self.button = QPushButton('Отправить')
        self.button.clicked.connect(self.send_message)
        layout.addWidget(self.button)

        self.response_label = QLabel('Ответ сервера:')
        layout.addWidget(self.response_label)

        self.setLayout(layout)

    def send_message(self):
        message = self.input.text()
        if not message:
            self.response_label.setText('Введите сообщение!')
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
                s.sendall(message.encode('utf-8'))
                data = s.recv(1024)
                self.response_label.setText(f'Сервер: {data.decode("utf-8")}')
            except ConnectionRefusedError:
                self.response_label.setText("Сервер не запущен!")
            except Exception as e:
                self.response_label.setText(f"Ошибка: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = ClientApp()
    client.show()
    sys.exit(app.exec())