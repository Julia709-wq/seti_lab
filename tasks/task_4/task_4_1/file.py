from cryptography.fernet import Fernet

# Однократно запускается для генерации ключа
def generate_key(filename="secret.key"):
    key = Fernet.generate_key()
    with open(filename, "wb") as f:
        f.write(key)
    print(f"Ключ сохранён в: {filename}")

def load_key(filename="secret.key"):
    with open(filename, "rb") as f:
        return f.read()

def encrypt_file(input_path, output_path, key_path="secret.key"):
    key = load_key(key_path)
    fernet = Fernet(key)

    with open(input_path, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    with open(output_path, "wb") as f:
        f.write(encrypted)

    print(f"Файл успешно зашифрован и сохранён в: {output_path}")


def decrypt_file(encrypted_path, output_path, key_path="secret.key"):
    key = load_key(key_path)
    fernet = Fernet(key)

    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()

    decrypted = fernet.decrypt(encrypted_data)

    with open(output_path, "wb") as f:
        f.write(decrypted)

    print(f"Файл успешно расшифрован и сохранён в: {output_path}")


# generate_key()
encrypt_file("original", "encrypted")
decrypt_file("encrypted", "decrypted")
