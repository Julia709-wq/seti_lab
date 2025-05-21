from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os


initial_text = "Сообщение для шифрования".encode('utf-8')

# генерация ключа и IV
key = os.urandom(32)  # 256 бит
iv = os.urandom(16)  # для CBC, CFB, OFB
nonce = os.urandom(12)  # для GCM

def pad(data):
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()

def unpad(data):
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(data) + unpadder.finalize()

def cbc_encrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded = pad(data)
    return encryptor.update(padded) + encryptor.finalize()

def cbc_decrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(data) + decryptor.finalize()
    return unpad(decrypted)

def cfb_encrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    return cipher.encryptor().update(data) + cipher.encryptor().finalize()

def cfb_decrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    return cipher.decryptor().update(data) + cipher.decryptor().finalize()

def ofb_encrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.OFB(iv), backend=default_backend())
    return cipher.encryptor().update(data) + cipher.encryptor().finalize()

def ofb_decrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.OFB(iv), backend=default_backend())
    return cipher.decryptor().update(data) + cipher.decryptor().finalize()

def gcm_encrypt(data, key, nonce):
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(data) + encryptor.finalize()
    return cipher_text, encryptor.tag

def gcm_decrypt(cipher_text, key, nonce, tag):
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(cipher_text) + decryptor.finalize()


print("CBC Mode")
cbc_encrypted = cbc_encrypt(initial_text, key, iv)
cbc_decrypted = cbc_decrypt(cbc_encrypted, key, iv)
print("Расшифровано:", cbc_decrypted.decode('utf-8'))

print("CFB Mode")
cfb_encrypted = cfb_encrypt(initial_text, key, iv)
cfb_decrypted = cfb_decrypt(cfb_encrypted, key, iv)
print("Расшифровано:", cfb_decrypted.decode('utf-8'))

print("OFB Mode")
ofb_encrypted = ofb_encrypt(initial_text, key, iv)
ofb_decrypted = ofb_decrypt(ofb_encrypted, key, iv)
print("Расшифровано:", ofb_decrypted.decode('utf-8'))

print("GCM Mode")
gcm_encrypted, tag = gcm_encrypt(initial_text, key, nonce)
gcm_decrypted = gcm_decrypt(gcm_encrypted, key, nonce, tag)
print("Расшифровано:", gcm_decrypted.decode('utf-8'))
