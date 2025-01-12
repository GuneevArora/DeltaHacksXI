
import streamlit as st
import cohere
from components import my_component


# Custom components
st.title("Security (Optional) Bot")



# AI Chat bot using Cohere
client = cohere.ClientV2(api_key=st.secrets['COHERE_API_KEY'])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

<<<<<<< Updated upstream
if prompt := st.chat_input("What is up?"):
=======

def ask_bot(messages, rerun = False):
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
    ], rerun=True)


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


            

st.header('Chat with our AI assistant')
if st.session_state['explain_leak'] is not None:
    explain_leak(st.session_state['explain_leak'])
    st.session_state['explain_leak'] = None
    st.session_state['skip'] = False

if prompt := st.chat_input("Ask a question:"):
>>>>>>> Stashed changes
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
with st.sidebar:
    my_component("Sup", key="foo")


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