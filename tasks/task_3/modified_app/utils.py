import os
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def generate_dh_parameters():
    parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
    return parameters

def serialize_parameters(parameters):
    return parameters.parameter_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.ParameterFormat.PKCS3
    )

def load_parameters(pem_bytes):
    return serialization.load_pem_parameters(pem_bytes, backend=default_backend())

def generate_private_key(parameters):
    return parameters.generate_private_key()

def get_public_bytes(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)

def load_public_key(pem_bytes):
    return serialization.load_pem_public_key(pem_bytes, backend=default_backend())

def derive_shared_key(private_key, peer_public_key):
    shared_secret = private_key.exchange(peer_public_key)
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'dh key exchange',
        backend=default_backend()
    ).derive(shared_secret)

def encrypt_message(message: str, key: bytes):
    nonce = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode('utf-8')) + encryptor.finalize()
    return nonce, ciphertext, encryptor.tag

def decrypt_message(nonce, ciphertext, tag, key):
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()
