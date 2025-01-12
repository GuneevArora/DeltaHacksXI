from typing import NamedTuple
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from leaked_sites import is_valid_email, check_email_leaks
import cohere
from react_components import icon_btn, pw_shower, pwn_card, vault
from passman import generate_pass, PWSetup, get_list as get_password_list, view_password, add_password
from url_checker import check_url_safety
from time import sleep
from enc import upload_to_vault, get_files_list, download_from_vault, vault_delete

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
if 'DOWN_DATA' not in st.session_state:
    st.session_state['DOWN_DATA'] = None

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
TO_SHOW = None
if 'show_quiz' not in st.session_state:
    st.session_state.show_quiz = True

# Function to hide the expander after completion
def hide_quiz():
    st.session_state.show_quiz = False

if st.session_state.show_quiz:

    answers = {}

    # Ask the user questions
    answers['vpn'] = st.radio("Are you using a VPN?",
                               ('Yes', 'No'),
                               index=None)  # Ensure no default selection

    answers['public wi-fi'] = st.radio("Do you connect to public Wi-Fi networks without a VPN?",
                                        ('Yes', 'No'),
                                        index=None)

    answers['browser'] = st.selectbox("Which browser are you using?",
                                       ['Select', 'Brave', 'Firefox', 'Safari', 'Edge', 'Chrome', 'Other'])

    answers['same password'] = st.radio("Do you always use the same password?",
                                         ('Yes', 'No'),
                                         index=None)

    answers['password complexity'] = st.radio("Do your passwords contain a mixture of symbols, letters, and numbers?",
                                               ('Yes', 'No'),
                                               index=None)

    answers['change password'] = st.radio("How often do you change your passwords?",
                                           ('Often', 'Only when needed', 'Never'),
                                           index=None)

    answers['2fa'] = st.radio("Have you enabled two-factor authentication (2FA) on your accounts?",
                               ('Yes', 'No'),
                               index=None)

    answers['social media privacy'] = st.radio("Are your social media profiles private?",
                                               ('Yes', 'No'),
                                               index=None)

    answers['share personal info'] = st.radio("Do you share personal information on the internet or social media?",
                                               ('Yes', 'No'),
                                               index=None)

    answers['antivirus'] = st.radio("Do you have antivirus or antimalware software installed on your devices?",
                                     ('Yes', 'No'),
                                     index=None)

    # Score map
    score_map = {
        'vpn': {'Yes': 10, 'No': 1},
        'public wi-fi': {'Yes': 1, 'No': 10},
        'browser': {'Brave': 10, 'Firefox': 8, 'Safari': 6, 'Edge': 5, 'Chrome': 3, 'Other': 3},
        'same password': {'Yes': 1, 'No': 10},
        'password complexity': {'Yes': 10, 'No': 1},
        'change password': {'Often': 10, 'Only when needed': 5, 'Never': 1},
        '2fa': {'Yes': 10, 'No': 1},
        'social media privacy': {'Yes': 10, 'No': 1},
        'share personal info': {'Yes': 1, 'No': 10},
        'antivirus': {'Yes': 10, 'No': 1}
    }

    def calculate_points(answers):
        points = 0
        points += score_map['vpn'][answers['vpn']]
        points += score_map['public wi-fi'][answers['public wi-fi']]

        # Handle the case where 'Select' is chosen and should map to 0 points
        browser_score = score_map['browser'].get(answers['browser'], 0)
        points += browser_score

        points += score_map['same password'][answers['same password']]
        points += score_map['password complexity'][answers['password complexity']]
        points += score_map['change password'][answers['change password']]
        points += score_map['2fa'][answers['2fa']]
        points += score_map['social media privacy'][answers['social media privacy']]
        points += score_map['share personal info'][answers['share personal info']]
        points += score_map['antivirus'][answers['antivirus']]

        return points

    # Button to calculate the score
    TO_SHOW = None
    if st.button("Submit"):
        if answers['browser'] == 'Select':  # You can easily check for 'Select' here
            st.warning("Please select a valid browser option.")
        else:
            total_score = calculate_points(answers)
            # Display the result
            st.write(f"Your total score is: {total_score} out of 100")

            TO_SHOW = answers, total_score
            hide_quiz()


if not st.session_state.show_quiz:
    if TO_SHOW is not None:
        if total_score == 100:
            st.success("Congratulations! You have a perfect score!")
            st.balloons()
        else:
            st.success("Quiz completed. Thank you, please wait for your personal safety tips!")
            if TO_SHOW is not None:
                personalized_prompt = (
                    f"In your security questionnaire, you answered: {answers}.\n"
                    f"Your total score is {total_score} out of 100.\n"
                    "Based on these answers, please provide personalized security tips."
                )
                if 'messages' not in st.session_state:
                    st.session_state.messages = []
                st.session_state.messages.append({"role": "user", "content": personalized_prompt})
                # Call your bot logic here (for demonstration, assumed as ask_bot function)
                ask_bot(st.session_state.messages)
                # Removed the personalized prompt from the session state
                st.session_state.messages.remove({"role": "user", "content": personalized_prompt})
                
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
        if file != "" :
            enc_submit = st.button("Submit")
        if enc_submit:
            upload_to_vault(file)
            st.text("File stored successfully!")
        
        fl = get_files_list()

        if st.session_state['DOWN_DATA'] is not None and st.session_state['DOWN_DATA']['f']:
            st.download_button(
                f'Click to Download {st.session_state["DOWN_DATA"]["f"]}',
                st.session_state['DOWN_DATA']['data'],
                st.session_state['DOWN_DATA']['f']
            )

        action = vault(get_files_list())
        if action is not None:
            dm = action['deleteMode']
            f = action['file']
            idx = action['idx']
            st.session_state['DOWN_DATA'] = None
            if dm:
                vault_delete(f)
            else:
                data = download_from_vault(f)
                st.session_state['DOWN_DATA'] = { 'data': data, 'f': f }
                st.rerun()

st.markdown(SIDE_BAR_STYLING, unsafe_allow_html=True)
st.session_state['skip'] = False
st.session_state['do_last'] = False
