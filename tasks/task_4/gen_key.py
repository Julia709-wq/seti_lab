from cryptography.fernet import Fernet

def generate_and_save_key(filename="secret.key"):
    key = Fernet.generate_key()
    with open(filename, "wb") as key_file:
        key_file.write(key)
    print(f"Ключ сохранён в {filename}")


generate_and_save_key()
