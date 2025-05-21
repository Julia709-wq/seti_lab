import socket
import threading

def handle_client(client_socket):
    """Обрабатывает соединение с клиентом в отдельном потоке"""
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            client_socket.sendall(message)
    finally:
        client_socket.close()

def start_server():
    """Запускает сервер и обрабатывает множество соединений"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9090))
    server_socket.listen()
    print("Сервер запущен и ожидает подключений...")

    while True:
        client_sock, address = server_socket.accept()
        print(f"Принято соединение от {address}")
        client_thread = threading.Thread(target=handle_client, args=(client_sock,))
        client_thread.start()


start_server()
