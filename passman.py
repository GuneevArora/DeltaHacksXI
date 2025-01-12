import streamlit as st
import cohere
import string
import random
import os
import json
from dataclasses import dataclass
import ard
import enc

_CLIENT = None

@dataclass
class PWSetup:
    min_length: int
    max_length: int
    symbols: int
    numbers: int
    caps: int


_MSGS = []
MODEL = 'command-r-08-2024'

_DB = None
F = '.vault/poasjdfhasidgbsab'

def load_db():
    global _DB
    if os.path.exists(F):
        with open(F, 'rb') as f:
            ee = enc.decrypt(f.read())
        _DB = json.loads(ee.decode())
    else:
        _DB = []
        save_db()

def get_pwdb():
    if _DB is None:
        load_db()
    return _DB

def save_db():
    global _DB
    ee = json.dumps(_DB).encode()
    with open(F, 'wb') as f:
        f.write(enc.encrypt(ee))

class TooManyRequests(Exception):
    def __init__(self):
        super().__init__('Generating too many passwords too fast is unsafe, as it reduces randomness and security. Please wait a minute.')

def getpw_client() -> cohere.ClientV2:
    global _CLIENT, _MSGS
    if _CLIENT is None:
        _CLIENT = cohere.ClientV2(api_key=st.secrets['COHERE_API_KEY'])
        _MSGS.append({ 'role': 'system', 'content': 'You are a random sentence generator, you reply only with the response no greetings. never repeat a sentence.' })
        _MSGS.append({ 'role': 'user', 'content': 'create a random sentence of 4 words each with a maximum of 6 letters' })
        _CLIENT.chat(model=MODEL, messages=_MSGS)
    return _CLIENT

def generate_pass(pws: PWSetup):
    global _MSGS
    ac = ''
    four_words = ''

    maxl = pws.max_length - (pws.symbols + pws.numbers)

    while len(ac) < pws.min_length:
        _MSGS.append({ 'role': 'user', 'content': 'create a different new random sentence of 4 words each with a maximum of 6 letters that is completely different to the last one' })
        try:
            four_words = getpw_client().chat(
                model = 'command-r-08-2024',
                messages=_MSGS
            ).message.content[0].text.splitlines()[0]
            four_words = ''.join(i for i in four_words if i in string.ascii_letters or i == ' ')
            ac = four_words.replace(' ', '')
        except cohere.TooManyRequestsError:
            raise TooManyRequests()
    if len(ac) > maxl:
        ac = ''.join(four_words.split(' ')[:3])
        if len(ac) < pws.min_length:
            ac = ''.join(four_words)[:maxl]
    ac = ac[:pws.caps].upper() + ac[pws.caps:].lower()
    symbols = ''.join(random.choice('?&<>%$!@') for i in range(pws.symbols))
    numbers = ''.join(random.choice(string.digits) for i in range(pws.symbols))
    sn = list(symbols + numbers)
    random.shuffle(sn)
    ac += ''.join(sn)
    return ac

def add_password(site: str, un: str, pw: str):
    db = get_pwdb()
    db.append({ 'site': site, 'username': un, 'password': pw })
    save_db()

def get_list():
    return [ { 'site': entry['site'], 'username': entry['username'] } for entry in get_pwdb() ]

def view_password(idx: int) -> str:
    db = get_pwdb()
    if len(db) <= idx:
        return "Password doesn't exist"
    ent = db[idx]
    try:
        ard.send_ard(ent['password'])
        return 'Password sent to viewing system.'
    except ConnectionRefusedError:
        return 'Viewing system disengaged'

