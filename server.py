import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Подключение от {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"Клиент {addr} отключился")
                    break
                print(f"Получено от {addr}: {data.decode('utf-8')}")
                conn.sendall('Сообщение получено'.encode('utf-8'))
