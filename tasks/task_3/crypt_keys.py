from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend

# генерация параметров
parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend)

# генерация ключей для Alice
alice_private_key = parameters.generate_private_key()
alice_public_key = alice_private_key.public_key()

# генерация ключей для Bob
bob_private_key = parameters.generate_private_key()
bob_public_key = bob_private_key.public_key()

# вычисление общего секретного ключа
alice_shared_key = alice_private_key.exchange(bob_public_key)
bob_shared_key = bob_private_key.exchange(alice_public_key)

if alice_shared_key == bob_shared_key:
    print("Обмен ключами прошел успешно.")
else:
    print("Общий секретный ключ не совпадает.")

