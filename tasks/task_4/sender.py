from cryptography.fernet import Fernet

def load_key(filename="secret.key"):
    with open(filename, "rb") as key_file:
        return key_file.read()

def encrypt_and_save_message(message, key_filename="secret.key", output_filename="encrypted_message.txt"):
    key = load_key(key_filename)
    cipher = Fernet(key)
    encrypted = cipher.encrypt(message.encode("utf-8"))

    with open(output_filename, "wb") as f:
        f.write(encrypted)

    print(f"Зашифрованное сообщение сохранено в {output_filename}")


msg = input("Введите сообщение для отправки: ")
encrypt_and_save_message(msg)
