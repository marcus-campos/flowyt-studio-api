import base64
from django.conf import settings

from cryptography.fernet import Fernet


class Cryptography:
    crypto_class = None

    def __init__(self):
        token = bytes(settings.SECRET_KEY.encode("utf-8"))
        self.crypto_class = Fernet(token)

    def encrypt(self, value):
        value = value.encode("utf-8")
        encripted = self.crypto_class.encrypt(value)
        return encripted.decode("utf-8")

    def decrypt(self, value):
        encoded = value.encode("utf-8")
        decrypted = self.crypto_class.decrypt(bytes(encoded))
        return decrypted.decode("utf-8")
