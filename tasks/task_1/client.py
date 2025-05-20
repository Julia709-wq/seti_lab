import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 9090))
        print("Подключено к серверу. Введите 'exit' для выхода.")

        while True:
            message = input("Введите команду или сообщение для сервера: ")
            if message.lower() == 'exit':
                print("Завершение работы.")
                break
            if message.lower() == 'shutdown':
                print("Отправка команды на завершение работы сервера")
                client_socket.sendall(message.encode('utf-8'))
                response = client_socket.recv(1024)
                print(f"Ответ от сервера: {response.decode('utf-8')}")
                break

            client_socket.sendall(message.encode('utf-8'))
            response = client_socket.recv(1024)
            print(f"Ответ от сервера: {response.decode('utf-8')}")

    except ConnectionRefusedError as e:
        print("Ошибка подключения: ", e)
    except socket.error as e:
        print("Ошибка сети: ", e)
    except KeyboardInterrupt:
        print("Подключение прервано вручную.")
    except Exception as e:
        print("Произошла ошибка: ", e)

    finally:
        client_socket.close()


start_client()
