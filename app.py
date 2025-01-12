from typing import NamedTuple
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import cohere
from react_components import icon_btn

if 'sidebar_state' not in st.session_state:
    st.session_state['sidebar_state'] = 'none'
if 'skip' not in st.session_state:
    st.session_state['skip'] = False

st.markdown('''
<style>
    div[data-testid="stSidebarCollapseButton"] {
        display: none!important;
    }
        
    div[data-testid="stSidebarUserContent"] {
        padding: 0px 0px !important;
    }
</style>
''', unsafe_allow_html=True)

EXPANDED_STYLING = '''
<style>
    .stSidebar {
        width: 300x!important;
        max-width: 300px!important;
        min-width: 300px!important;
    }
</style>
'''
COLAPSED_STYLING = '''
<style>
    .stSidebar {
        width: 100px!important;
        max-width: 100px!important;
        min-width: 100px!important;
    }
</style>
'''


SIDE_BAR_STYLING = None
if st.session_state['sidebar_state'] == 'none':
    SIDE_BAR_STYLING = COLAPSED_STYLING
else:
    SIDE_BAR_STYLING = EXPANDED_STYLING

def change_sidebar(tab: str):
    st.session_state['sidebar_state'] = tab

def toggle_sidebar(tab: str):
    global SIDE_BAR_STYLING
    if st.session_state['skip']:
        st.session_state['skip'] = False
        return
    if st.session_state['sidebar_state'] == tab:
        st.session_state['sidebar_state'] = 'none'
    else:
        st.session_state['sidebar_state'] = tab
    st.session_state['skip'] = True
    st.rerun()

# Custom components
st.title("Security (Optional) Bot")

# AI Chat bot using Cohere
client = cohere.ClientV2(api_key=st.secrets['COHERE_API_KEY'])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        res = client.chat(
            model='command-r-plus-08-2024',
            messages=st.session_state.messages
        )
    
        response = res.message.content[0].text
        st.markdown(response)
    st.session_state.messages.append({ 'role': 'assistant', 'content': response })


# Sidebar

icon_col, tab_col = None, None

if st.session_state['sidebar_state'] == 'none':
    icon_col = st.sidebar.columns([1])[0]
else:
    icon_col,tab_col = st.sidebar.columns([100/300, 1 - 100/300])


# (icon,key,tab)
Tab = NamedTuple('Tab', [('icon',str),('tab',str)])
TABS = [
    Tab('/email_icon.png','leak'),
    Tab('/password_icon.png','pwman'),
    Tab('/url_icon.png','safe'),
    Tab('/vault_icon.png','vault'),
]

with icon_col:
    for icon,tab in TABS:
        ibv = icon_btn(src=icon, key=tab)

        print(tab, 'BTN state', ibv)
        if ibv == 1:
            toggle_sidebar(tab)

st.markdown(SIDE_BAR_STYLING, unsafe_allow_html=True)
