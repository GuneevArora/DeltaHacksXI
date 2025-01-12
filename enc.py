#File encrytion and decryption
import cryptography
from cryptography.fernet import Fernet
import hashlib
import os
import random
import json

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

_DB_FILE = '.vault/asfsdafsilWG2pz4C'
def save_db():
    global _DB
    with open(_DB_FILE, 'wb') as f:
            f.write(encrypt(json.dumps(_DB).encode()))

def get_db():
    global _DB
    if _DB is None:
        if not os.path.exists(_DB_FILE):
            _DB = {'OTN':{},'NTO':{},'F_H':{}}
            save_db()
        else:
            _DB = json.loads(decrypt(open(_DB_FILE, 'rb').read()).decode())
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

def upload_data_to_vault(filepath: str, data: bytes):
    encrypted = encrypt(data)
    nf = f'.vault/{random_generator()}'
    with open(nf, 'wb') as f:
        f.write(encrypted)
    
    fh = hash_gen(nf)
    db = get_db()
    db['OTN'][filepath] = nf
    db['NTO'][nf] = filepath
    db['F_H'][filepath] = fh

def upload_to_vault(file):
    upload_data_to_vault(file.name, file.read())

def download_from_vault(file: str) -> bytes:
    ofn = get_db()['OTN'][file]
    with open(ofn, 'rb') as f:
        ee = f.read()
    return get_key().decrypt(ee)

def files_list():
    return list(get_db()['OTN'].keys())

#File Integrity Checker to 
def hash_gen(file):
    with open(file, 'rb') as f:
        data = f.read()
    
    file_hash = hashlib.sha256(data).hexdigest()    

    return file_hash

def verify_file_integrity(file, original_hash):
    current_hash = hash_gen(file)
    return current_hash == original_hash

    



    