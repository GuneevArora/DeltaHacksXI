import streamlit
import streamlit.components.v1 as components


_icon_btn = components.declare_component('iconbtn', url='http://localhost:3001/icon_btn')
def icon_btn(src: str, key: str) -> bool:
    return _icon_btn(src=src, key=key, value=False)

