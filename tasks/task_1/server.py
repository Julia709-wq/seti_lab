import socket
import logging
import sys

logger = logging.getLogger('server')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('../logs/server.log')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind(('localhost', 9090))
        server_socket.listen()
        logger.info("The server is running.")
        print("Сервер запущен и ожидает подключений...")

        while True:
            client_socket, client_address = server_socket.accept()
            logger.info(f"Client connected: {client_address}")

            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        print("Клиент закрыл соединение.")
                        break

                    if data.decode('utf-8').lower() == 'shutdown':
                        print("Получена команда shutdown. Завершение работы сервера...")
                        client_socket.sendall(b"Server is shutting down...")
                        return
                    client_socket.sendall(data)

            except ConnectionResetError:
                print("Клиент неожиданно разорвал соединение.")
            except Exception as e:
                print("Ошибка при работе с клиентом: ", e)

            finally:
                client_socket.close()

    except KeyboardInterrupt:
        print("Сервер остановлен вручную.")
    except Exception as e:
        print("Ошибка сервера: ", e)

    finally:
        print("Сервер завершил работу")
        server_socket.close()
        sys.exit(0)



start_server()
