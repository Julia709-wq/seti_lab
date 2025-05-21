from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


# генерация параметров
parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())

# генерация пары ключей
"""приватный ключ используется для вычисления публичного ключа и, 
    в дальнейшем, для генерации общего секретного ключа, который будет 
    использоваться для шифрования данных"""
private_key = parameters.generate_private_key()
public_key = private_key.public_key()

# вычисление общего секретного ключа
# shared_secret = private_key.exchange(other_public_key)
# derived_key = HKDF(
#     algoritm=hashes.SHA256(),
#     length=32,
#     salt=None,
#     info=b'handshake data',
#     backend=default_backend()
# ).derive(shared_secret)
