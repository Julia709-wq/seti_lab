import socket

def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 9090)

    print("Введите exit для завершения работы.")

    try:
        while True:
            message = input("Введите сообщение для сервера: ")
            client_socket.sendto(message.encode('utf-8'), server_address)
            response, _ = client_socket.recvfrom(1024)
            print(f"Ответ от сервера: {response.decode()}")

            if message.lower() == 'exit':
                print("Завершение работы...")
                break

    except KeyboardInterrupt:
        print("Работа клиента прервана вручную.")
    finally:
        client_socket.close()
        print("Сокет клиента закрыт.")


udp_client()
