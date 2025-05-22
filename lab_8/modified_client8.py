import socket
from utils8 import *


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9090))

    # получение параметров от сервера
    param_bytes = client_socket.recv(4096)
    parameters = load_parameters(param_bytes)

    # генерация ключей
    client_private = generate_private_key(parameters)
    client_public = client_private.public_key()

    # получение открытого ключа сервера
    server_pub_bytes = client_socket.recv(4096)
    server_public = load_public_key(server_pub_bytes)

    # отправление своего
    client_socket.sendall(get_public_bytes(client_public))
    # вычисление общего ключа
    key = derive_shared_key(client_private, server_public)

    print("Соединение установлено. Шифрование активно.")

    try:
        while True:
            message = input("Введите команду или сообщение для сервера: ")
            if message.lower() == 'exit':
                print("Завершение работы.")
                break

            nonce, cipher_text, tag = encrypt_message(message, key)
            client_socket.sendall(nonce + tag + cipher_text)

            header = client_socket.recv(12 + 16)
            nonce = header[:12]
            tag = header[12:]
            response = client_socket.recv(1024)
            decrypted = decrypt_message(nonce, response, tag, key)
            print(f"Ответ от сервера: {decrypted.decode('utf-8')}")

    finally:
        client_socket.close()


start_client()
