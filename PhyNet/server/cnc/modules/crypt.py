from cryptography.fernet import Fernet


class Crypt():

    def __init__(self, enckey: str=""):
        self.f=Fernet(enckey)

    def encryptD(self, msg: str):
        msg=self.f.encrypt(msg)
        return msg

    def decryptD(self, msg: str):
        msg=self.f.decrypt(msg)
        return msg