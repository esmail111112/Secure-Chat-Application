from cryptography.fernet import Fernet

class SecureChat:
    def __init__(self, key=None):
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.cipher = Fernet(self.key)

    def encrypt(self, message):
        return self.cipher.encrypt(message.encode())

    def decrypt(self, message):
        return self.cipher.decrypt(message).decode()
