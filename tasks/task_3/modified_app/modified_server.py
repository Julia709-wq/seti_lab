import socket
import logging
from utils import *


logger = logging.getLogger('server')
logger.setLevel(logging.INFO)
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

file_handler = logging.FileHandler(os.path.join(log_dir, 'modified_server.log'))
# file_handler = logging.FileHandler('tasks/task_3/modified_app/logs/modified_server.log')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9090))
    server_socket.listen()
    logger.info("The server is running.")
    print("Сервер запущен и ожидает подключений...")

    try:
        client_socket, client_address = server_socket.accept()
        logger.info(f"Client connected: {client_address}")

        # генерация параметров и отправка клиенту
        parameters = generate_dh_parameters()
        param_bytes = serialize_parameters(parameters)
        client_socket.sendall(param_bytes)

        # ключи
        server_private = generate_private_key(parameters)
        server_public = server_private.public_key()
        client_socket.sendall(get_public_bytes(server_public))

        # получение клиентского ключа
        client_pub_bytes = client_socket.recv(4096)
        client_public = load_public_key(client_pub_bytes)
        key = derive_shared_key(server_private, client_public)

        print("Общий ключ установлен")

        while True:
            header = client_socket.recv(12 + 16)
            if not header:
                break
            nonce = header[:12]
            tag = header[12:]
            cipher_text = client_socket.recv(1024)
            message = decrypt_message(nonce, cipher_text, tag, key).decode('utf-8')

            print(f"Зашифрованное сообщение: {message}")
            if message.lower() == 'shutdown':
                print("Получена команда shutdown. Завершение работы...")
                break

            nonce, cipher_text, tag = encrypt_message(f"Получено сообщение: {message}", key)
            client_socket.sendall(nonce + tag + cipher_text)

    finally:
        server_socket.close()


start_server()
