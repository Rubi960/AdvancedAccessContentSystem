import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def get_random_key() -> bytes:
    return AESGCM.generate_key(bit_length=128)


def remove_extra(c: bytes) -> bytes:
    n = int(c[-1]) + 1
    return c[: len(c) - n]


def complete_block(m: bytes) -> bytes:
    block_size = 16
    remaining = block_size - (len(m) % block_size)
    return m + ((remaining-1).to_bytes() * remaining)


def encrypt_aes(k: bytes, m: bytes) -> bytes:
    # Generate a random 128-bit IV.
    iv = os.urandom(16)

    # Construct an AES-128-CBC Cipher object with the given key and a
    # randomly generated IV.
    encryptor = Cipher(
        algorithms.AES(k),
        modes.CBC(iv),
        backend=default_backend()
    ).encryptor()

    # Encrypt the plaintext and get the associated ciphertext.
    ciphertext = encryptor.update(m) + encryptor.finalize()
    return iv, ciphertext


def decrypt_aes(k: bytes, iv: bytes, c: bytes) -> bytes:
    # Construct a Cipher object, with the key, iv
    decryptor = Cipher(
        algorithms.AES(k),
        modes.CBC(iv),
        backend=default_backend()
    ).decryptor()
    # Decryption gets us the plaintext.
    return decryptor.update(c) + decryptor.finalize()
