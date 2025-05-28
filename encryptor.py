# encryptor.py
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

class Encryptor:
    def __init__(self):
        self.key_pair = RSA.generate(2048)
        self.public_key = self.key_pair.publickey()

    def export_public_key(self):
        return self.public_key.export_key()

    def load_peer_public_key(self, key_bytes):
        self.peer_public_key = RSA.import_key(key_bytes)

    def encrypt(self, message: bytes) -> bytes:
        cipher = PKCS1_OAEP.new(self.peer_public_key)
        return cipher.encrypt(message)

    def decrypt(self, encrypted: bytes) -> bytes:
        cipher = PKCS1_OAEP.new(self.key_pair)
        return cipher.decrypt(encrypted)
