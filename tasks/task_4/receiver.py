from cryptography.fernet import Fernet

def load_key(filename="secret.key"):
    with open(filename, "rb") as key_file:
        return key_file.read()

def read_and_decrypt_message(key_filename="secret.key", input_filename="encrypted_message.txt"):
    key = load_key(key_filename)
    cipher = Fernet(key)

    with open(input_filename, "rb") as f:
        encrypted = f.read()

    decrypted = cipher.decrypt(encrypted)
    print("Расшифрованное сообщение:", decrypted.decode("utf-8"))


read_and_decrypt_message()
