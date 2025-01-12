
import streamlit as st
import cohere
from react_components import icon_btn



if 'sidebar_state' not in st.session_state:
    st.session_state['sidebar_state'] = 'none'

def change_sidebar(tab: str):
    st.session_state['sidebar_state'] = tab

def toggle_sidebar(tab: str):
    if st.session_state['sidebar_state'] == tab:
        st.session_state['sidebar_state'] = 'none'
    else:
        st.session_state['sidebar_state'] = tab

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
        print('COHERE response:', response)
        st.markdown(response)
    st.session_state.messages.append({ 'role': 'assistant', 'content': response })


# Sidebar

icon_col, tab_col = None, None

if st.session_state['sidebar_state'] == 'none':
    icon_col,tab_col = st.sidebar.columns([75/280, 1 - 75/280])
else:
    icon_col = st.sidebar.columns([1])

with icon_col:
    if icon_btn(src='/icon.png'):
        toggle_sidebar('goggle')

if st.session_state['sidebar_state'] == 'none':
    st.markdown('''
    <style>
        .sidebar-content {
            width: 80px;
        }
    </style>
    ''')
else:
    st.markdown('''
    <style>
        .sidebar-content {
            width: 300px;
        }
    </style>
    ''')


# Custom CSS
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 600px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)