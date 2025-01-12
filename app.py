from typing import NamedTuple
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from leaked_sites import is_valid_email, check_email_leaks
import cohere
from react_components import icon_btn, pw_shower, pwn_card
from passman import generate_pass, PWSetup, get_list as get_password_list, view_password, add_password
from url_checker import check_url_safety
from time import sleep
from enc import encrypt, decrypt, verify_file_integrity, generate_key, upload_to_vault

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'sidebar_state' not in st.session_state:
    st.session_state['sidebar_state'] = 'none'
if 'skip' not in st.session_state:
    st.session_state['skip'] = False
if 'explain_leak' not in st.session_state:
    st.session_state['explain_leak'] = None
if 'VIEW_PASS' not in st.session_state:
    st.session_state['VIEW_PASS'] = -1

@st.dialog('Info')
def modal(mes: str):
    st.write(mes)

st.markdown('''
<style>
    div[data-testid="stSidebarCollapseButton"] {
        display: none!important;
    }
        
    div[data-testid="stSidebarUserContent"] {
        @apply p-4;
    }
    
    div[data-testid="stTextInputRootElement"] {
        @apply mt-60 !important;
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


def ask_bot(messages):
    res = client.chat(
        model='command-r-plus-08-2024',
        messages=messages
    )
    response = res.message.content[0].text
    st.session_state['messages'].append({ 'role': 'assistant', 'content': response })
    with st.chat_message("assistant"):
        st.markdown(response)

def explain_leak(leak_source):
    new_msg = ''
    if leak_source.date is not None and len(leak_source.date) > 0:
        new_msg = f'Can you tell me about the data breach at {leak_source.site_name} on {leak_source.date}'
    else:
        new_msg = f'Can you tell me about the data breach at {leak_source.site_name}'
    ask_bot([
        { 'role': 'system', 'content': 'You are a bot that reports on data breaches and explain why and what happend. Only respond with answers in line with the topic, do not stray away from data breaches. Do not make up answers.'},
        { 'role': 'user', 'content': new_msg }
    ])


if st.session_state['explain_leak'] is not None:
    explain_leak(st.session_state['explain_leak'])
    st.session_state['explain_leak'] = None
    st.session_state['skip'] = False

if prompt := st.chat_input("Ask a question:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    ask_bot(st.session_state.messages)

# Sidebar

icon_col, tab_col = None, None

if st.session_state['sidebar_state'] == 'none':
    icon_col = st.sidebar.columns([1])[0]
else:
    icon_col,tab_col = st.sidebar.columns([100/600, 1 - 100/600])

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
        if ibv == 1:
            toggle_sidebar(tab)

if st.session_state['sidebar_state'] == "leak":
    with tab_col:
        email = st.text_input("Insert Email", key="email-input")

        if st.button('Go') or email:
            if is_valid_email(email):
                output = check_email_leaks(email)
                if len(output) == 0:
                    st.balloons()
                    st.success("Congratulations! No email leaks have been found!")
                else:
                    for i,out in enumerate(output):
                        pc = pwn_card(header=out.site_name, body=out.date, key=str(i))
                        if pc == 1:
                            if st.session_state['skip']:
                                continue
                            else:
                                st.session_state['explain_leak'] = out
                                st.session_state['skip'] = True
                                sleep(10)
            else:
                st.error("Email Not Valid!")
elif st.session_state['sidebar_state'] == 'pwman':
    if st.session_state['VIEW_PASS'] != -1:
        modal(view_password(st.session_state['VIEW_PASS']))
        st.session_state['VIEW_PASS'] = -1

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

        st.header('Saved Passwords')

        site = st.text_input('site')
        username = st.text_input('username/email', value='')
        password = st.text_input('password', value='')
        if st.button('Save password'):
            add_password(site, username, password)

        pw_c = pw_shower(get_password_list())
        if pw_c is not None and pw_c != -1:
            st.session_state['VIEW_PASS'] = pw_c
            st.rerun()
elif st.session_state['sidebar_state'] == 'safe':
    with tab_col:
        st.header('Is that a safe URL?')
        url = st.text_input(label='url', )
        if st.button('Go'):
            res = check_url_safety(url)
            if res['malicious']:
                st.text('This website is flagged for being malicious.')
                st.text('Flagged for the following')
                st.markdown('\n'.join(f'- {threat}' for threat in res['threats']))
                st.text('Flagged on the following platforms')
                st.markdown('\n'.join(f'- {platform}' for platform in res['platforms']))
            else:
                st.text('This website is NOT currently flagged for being malicious.')

#the encryption vault
elif st.session_state['sidebar_state'] == 'vault':
    with tab_col:
        st.header('Encrypt Files in Vault:')
        file = st.file_uploader("Drop Files Here:")
        if file != "" : enc_submit = st.button("Submit")
        if enc_submit:
            key = generate_key()
            upload_to_vault(file)
            st.text("File stored successfully! Here is your key: ", key)
                


        
        
            


st.markdown(SIDE_BAR_STYLING, unsafe_allow_html=True)
st.session_state['skip'] = False
st.session_state['do_last'] = False