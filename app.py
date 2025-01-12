from typing import NamedTuple
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from leaked_sites import is_valid_email, check_email_leaks
import cohere
from react_components import icon_btn, pwn_card
from passman import generate_pass, PWSetup

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
        @apply p-4;
    }
</style>
''', unsafe_allow_html=True)

EXPANDED_STYLING = '''
<style>
    .stSidebar {
        width: 600x!important;
        max-width: 600px!important;
        min-width: 600px!important;
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
st.title("NδtHacked")

# AI Chat bot using Cohere
client = cohere.ClientV2(api_key=st.secrets['COHERE_API_KEY'])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def ask_bot(prompt):

    with st.chat_message("assistant"):
        res = client.chat(
            model='command-r-plus-08-2024',
            messages=st.session_state.messages
        )
    
        response = res.message.content[0].text
        st.markdown(response)
    st.session_state.messages.append({ 'role': 'assistant', 'content': response })

if prompt := st.chat_input("Ask a question:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    ask_bot(prompt)
    


# Sidebar

icon_col, tab_col = None, None

if st.session_state['sidebar_state'] == 'none':
    icon_col = st.sidebar.columns([1])[0]
else:
    icon_col,tab_col = st.sidebar.columns([100/600, 1 - 100/600])

if st.session_state['sidebar_state'] == "leak":
    with tab_col:
        if email := st.chat_input("Insert Email", key="email-input"):
            if is_valid_email(email):
                output = check_email_leaks(email)
                if len(output) == 0:
                    st.balloons()
                    st.success("Congratulations! No email leaks have been found!")
                else:
                    for i in range(0,len(output)):
                        # renders pwn card. returns true if button is clicked, where bot is asked about a chosen data leak
                        pc = pwn_card(header=output[i].site_name, body=output[i].date, key="pwncard"+ str(i))
                        if pc == 1:
                            prompt = "Tell me about the " + output[i].site_name + " data leak on " + output[i].date
                            ask_bot(prompt)
            else:
                st.error("Email Not Valid!")



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

if st.session_state['sidebar_state'] == 'pwman':
    with tab_col:

        with st.expander('Password Generator'):
            mil = st.number_input(label='Minimum chars', value=6)
            mal = st.number_input(label='Maximum chars', value=20)
            sn  = st.number_input(label='# of Special chars', value=1)
            nn  = st.number_input(label='# of Numerical chars', value=1)
            cn  = st.number_input(label='# of Capital chars', value=1)

            if st.button(label='Generate Password'):
                pg = generate_pass(PWSetup(mil, mal, sn, nn, cn))
                st.text(pg)


st.markdown(SIDE_BAR_STYLING, unsafe_allow_html=True)
