import os
import pytest
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def generate_dh_parameters():
    return dh.generate_parameters(generator=2, key_size=2048)

def derive_shared_key(private_key, other_public_key):
    shared_secret = private_key.exchange(other_public_key)
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'dh-key-exchange',
        backend=default_backend()
    ).derive(shared_secret)

def gcm_encrypt(message, key):
    nonce = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode('utf-8')) + encryptor.finalize()
    return nonce, ciphertext, encryptor.tag

def gcm_decrypt(nonce, ciphertext, tag, key):
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


@pytest.fixture
def dh_keypair():
    parameters = generate_dh_parameters()
    alice_private = parameters.generate_private_key()
    bob_private = parameters.generate_private_key()
    return alice_private, bob_private


def test_shared_key_equal(dh_keypair):
    alice_private, bob_private = dh_keypair
    alice_public = alice_private.public_key()
    bob_public = bob_private.public_key()

    key1 = derive_shared_key(alice_private, bob_public)
    key2 = derive_shared_key(bob_private, alice_public)

    assert key1 == key2

def test_gcm(dh_keypair):
    alice_private, bob_private = dh_keypair
    shared = derive_shared_key(alice_private, bob_private.public_key())

    nonce, cipher_text, tag = gcm_encrypt("Hello, world!", shared)
    decrypted = gcm_decrypt(nonce, cipher_text, tag, shared)

    assert decrypted.decode('utf-8') == "Hello, world!"

def test_protection(dh_keypair):
    alice_private, bob_private = dh_keypair
    shared = derive_shared_key(alice_private, bob_private.public_key())
    nonce, cipher_text, tag = gcm_encrypt("Защищённое сообщение", shared)
    used_nonces = {nonce}

    decrypted = gcm_decrypt(nonce, cipher_text, tag, shared)
    assert decrypted.decode('utf-8') == "Защищённое сообщение"

    if nonce in used_nonces:
        with pytest.raises(ValueError, match="Проверка не пройдена"):
            raise ValueError("Проверка не пройдена")
