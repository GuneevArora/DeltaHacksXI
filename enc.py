#File encrytion and decryption
import cryptography
from cryptography.fernet import Fernet



def generate_key():
    key= Fernet.generate_key()
    with open('files.key', 'wb') as keysFile:
        keysFile.write(key)
    return key


def load_key():
    return open('files.key', 'rb').read()

#Encrypt the file
def encrypt(file, key):
    key_data = Fernet(key)
    with open(file, 'rb') as f:
        data = f.read()

    encrypted_data = key_data.encrypt(data)
    with open(file, 'wb') as f:
        f.write(encrypted_data)

    return encrypted_data

#Decrypt the file
def decrypt(file, key):
    key_data = Fernet(key)
    with open(file, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = key_data.decrypt(encrypted_data)
    with open(file, 'wb') as f:
        f.write(decrypted_data)

    return decrypted_data




    