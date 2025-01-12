#File encrytion and decryption
import cryptography
from cryptography.fernet import Fernet
import hashlib
import os
import random

if not os.path.exists('.vault'):
    os.makedirs('.vault')

_DB = None
_KEY = None

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%*_="

def random_generator():
    password = ''.join(random.choice(chars) for _ in range(17))
    return password


def generate_key():
    key= Fernet.generate_key()
    with open('silWG2pz4C!KQ3JDP.key', 'wb') as keysFile:
        keysFile.write(key)
    return key



def load_key():
    return open('silWG2pz4C!KQ3JDP.key', 'rb').read()

def get_key():
    global _KEY

    if _KEY is None:
        if not os.path.exists('silWG2pz4C!KQ3JDP.key'):
            _KEY = generate_key()
        else:
            _KEY = Fernet(load_key())
    
    return _KEY

def get_db():
    global _DB
    
    if _DB is None:
        _DB = {'OTN':{},'NTO':{},'F_H':{}}
    #encrypt the database
    key = get_key()
    encrypted_db = encrypt('.vault/j9xyrhffSaKepY7B8', key)
    with open('.vault/', 'wb') as f:
        f.write(encrypted_db)

    return _DB


def generate_key():
    key= Fernet.generate_key()
    with open('silWG2pz4C!KQ3JDP.key', 'wb') as keysFile:
        keysFile.write(key)
    return key


def encrypt(data: bytes) -> bytes:
    key = get_key()
    return key.encrypt(data)

def decrypt(data: bytes) -> bytes:
    key = get_key()
    return key.decrypt(data)

def upload_to_vault(file: str):
    with open(file, 'rb') as f:
        encrypted = encrypt(f.read())
    nf = random_generator()
    with open(nf, 'wb') as f:
        f.write(encrypted)
    
    fh = hash_gen(file)
    db = get_db()
    db['OTN'][file] = nf
    db['NTO'][nf] = file
    db['F_H'][file] = fh
    return True

#Decrypt the file TODO
# def decrypt(file, key):
#     key_data = Fernet(key)
#     with open(file, 'rb') as f:
#         encrypted_data = f.read()

#     decrypted_data = key_data.decrypt(encrypted_data)
#     new_file = random_generator()
#     with open(new_file, 'wb') as f:
#         f.write(decrypted_data)

#     db = get_db()
#     db['NTO'][new_file] = file

#     return decrypted_data

#File Integrity Checker to 
def hash_gen(file):
    with open(file, 'rb') as f:
        data = f.read()
    
    file_hash = hashlib.sha256(data).hexdigest()    

    return file_hash

def verify_file_integrity(file, original_hash):
    current_hash = hash_gen(file)
    return current_hash == original_hash

    



    