import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

used_nonces = set()  

# генерация ключа (в реальной системе — из DH)
key = os.urandom(32)

def send_message(message: str):
    message_bytes = message.encode('utf-8')
    nonce = os.urandom(12)  # 12 байт — стандартный размер для GCM

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message_bytes) + encryptor.finalize()
    return nonce, ciphertext, encryptor.tag

def receive_message(nonce, ciphertext, tag):
    if nonce in used_nonces:
        raise ValueError("Проверка не пройдена: этот nonce уже использовался!")
    used_nonces.add(nonce)

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted.decode('utf-8')


# отправитель
nonce, ciphertext, tag = send_message("Обращение отправителя.")

# получатель
msg = receive_message(nonce, ciphertext, tag)
print("Сообщение принято:", msg)

# повторная атака
try:
    replay = receive_message(nonce, ciphertext, tag)
except ValueError as e:
    print(e)
