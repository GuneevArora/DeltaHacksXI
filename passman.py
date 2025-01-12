import streamlit as st
import cohere
import string
import random
from dataclasses import dataclass

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

