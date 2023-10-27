#pip install pycrypto --user
# pip install pycryptodome
#post website
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import Padding
import binascii

class AESCipher(object):
    def __init__(self, key,iv):
        self.key = key
        self.iv = iv

    def encrypt(self, plaintext):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))
        encryptor = cipher.encryptor()

        plaintext = Padding.appendPadding(plaintext, blocksize=Padding.AES_blocksize, mode='CBC')
        raw = bytes(plaintext, 'utf-8')

        encoded = encryptor.update(raw) + encryptor.finalize()
        return encoded

    def decrypt(self, raw):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(raw) + decryptor.finalize()
        decrypted = str(decrypted, 'utf-8')
        decrypted = Padding.removePadding(decrypted, mode='ECB')

        return decrypted



#key = os.urandom(32)
#iv = os.urandom(16)

#cipher = AESCipher(key,iv)


# plaintext = "this is a super important message!!"
# encrypted = cipher.encrypt(plaintext)
# print('Encrypted:', encrypted)
#
# decrypted = cipher.decrypt(encrypted)
# print('Decrypted:', decrypted)