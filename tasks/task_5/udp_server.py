import socket

def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 9090))

    print("UDP сервер запущен и ожидает сообщений...")

    try:
        while True:
            message, client_address = server_socket.recvfrom(1024)
            print(f"Получено сообщение от {client_address}: {message.decode()}")
            server_socket.sendto(message, client_address)

            if message.decode().lower() == 'exit':
                print("Получена команда выхода. Завершение работы сервера...")
                server_socket.sendto("Сервер завершает работу.".encode(), client_address)
                break

            server_socket.sendto(message, client_address)

    except KeyboardInterrupt:
        print("Подключение прервано вручную.")
    finally:
        server_socket.close()
        print("Сервер остановлен. Сокет закрыт.")


udp_server()
