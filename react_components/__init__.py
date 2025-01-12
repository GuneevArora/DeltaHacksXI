
import streamlit.components.v1 as components


_icon_btn = components.declare_component('iconbtn', url='http://localhost:3001/icon_btn')
def icon_btn(src: str, key: str) -> bool:
    return _icon_btn(src=src, key=key)

_pwn_card = components.declare_component('pwncard', url='http://localhost:3001/pwn_card')
def pwn_card(header, body, key=None) -> bool:
    return _pwn_card(header = header, body = body, key = key, value=0)

_pw_shower = components.declare_component('pw_shower', url='http://localhost:3001/pw_shower')
def pw_shower(entries):
    return _pw_shower(entries=entries)

