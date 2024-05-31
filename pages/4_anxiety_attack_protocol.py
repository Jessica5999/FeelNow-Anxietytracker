import streamlit as st
import bcrypt
import binascii
import pytz
import datetime
import pandas as pd
from github_contents import GithubContents
from deep_translator import GoogleTranslator
import time

# Constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'password']
LANGUAGES = {
    "English": "en",
    "German": "de",
    "Spanish": "es",
    "French": "fr",
    "Chinese": "zh-cn"
}

@st.cache_resource
def get_github_contents():
    return GithubContents(
        st.secrets["github"]["owner"],
        st.secrets["github"]["repo"],
        st.secrets["github"]["token"]
    )

@st.cache_resource
def translate_text(text, target_language):
    translator = GoogleTranslator(target=target_language)
    return translator.translate(text)

def init_credentials():
    github = st.session_state.github
    if github.file_exists(DATA_FILE):
        return github.read_df(DATA_FILE)
    return pd.DataFrame(columns=DATA_COLUMNS)

def authenticate(username, password, users_df):
    if username in users_df['username'].values:
        stored_hashed_password = users_df.loc[users_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes):
            return True
    return False

def main():
    st.session_state.github = get_github_contents()
    st.session_state.df_users = init_credentials()
    
    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False

    if 'target_language' not in st.session_state:
        selected_language = st.selectbox("Choose your language", list(LANGUAGES.keys()), index=0)
        st.session_state['target_language'] = LANGUAGES[selected_language]
    else:
        st.write(translate_text("Language: ", st.session_state['target_language']) + st.session_state['target_language'])

    if not st.session_state['authentication']:
        options = st.sidebar.selectbox(translate_text("Select a page", st.session_state['target_language']),
                                       [translate_text("Login", st.session_state['target_language']),
                                        translate_text("Register", st.session_state['target_language'])])
        if options == translate_text("Login", st.session_state['target_language']):
            login_page()
        elif options == translate_text("Register", st.session_state['target_language']):
            register_page()
    else:
        st.sidebar.write(translate_text("Logged in as ", st.session_state['target_language']) + st.session_state['username'])
        anxiety_attack_protocol()
        if st.sidebar.button(translate_text("Logout", st.session_state['target_language'])):
            st.session_state['authentication'] = False
            st.session_state.pop('username', None)
            switch_page("main.py")

def login_page():
    st.title(translate_text("Login", st.session_state['target_language']))
    with st.form(key='login_form'):
        username = st.text_input(translate_text("Username", st.session_state['target_language']))
        password = st.text_input(translate_text("Password", st.session_state['target_language']), type="password")
        if st.form_submit_button(translate_text("Login", st.session_state['target_language'])):
            if authenticate(username, password, st.session_state.df_users):
                st.session_state['authentication'] = True
                st.session_state['username'] = username
                st.success(translate_text('Login successful', st.session_state['target_language']))
                st.experimental_rerun()
            else:
                st.error(translate_text('Incorrect username or password', st.session_state['target_language']))

def register_page():
    st.title(translate_text("Register", st.session_state['target_language']))
    with st.form(key='register_form'):
        new_username = st.text_input(translate_text("New Username", st.session_state['target_language']))
        new_name = st.text_input(translate_text("Name", st.session_state['target_language']))
        new_password = st.text_input(translate_text("New Password", st.session_state['target_language']), type="password")
        if st.form_submit_button(translate_text("Register", st.session_state['target_language'])):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
            hashed_password_hex = binascii.hexlify(hashed_password).decode()
            if new_username in st.session_state.df_users['username'].values:
                st.error(translate_text("Username already exists. Please choose a different one.", st.session_state['target_language']))
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                st.session_state.github.write_df(DATA_FILE, st.session_state.df_users, "added new user")
                st.success(translate_text("Registration successful! You can now log in.", st.session_state['target_language']))

def anxiety_attack_protocol():
    username = st.session_state['username']
    data_file = f"{username}_data.csv"
    if 'data' not in st.session_state:
        if st.session_state.github.file_exists(data_file):
            st.session_state.data = st.session_state.github.read_df(data_file)
        else:
            st.session_state.data = pd.DataFrame(columns=['Date', 'Time', 'Severity', 'Symptoms', 'Triggers', 'Help'])

    st.title(translate_text("Anxiety Attack Protocol", st.session_state['target_language']))
    date_selected = st.date_input(translate_text("Date", st.session_state['target_language']), value=datetime.date.today())
    add_time_severity()

    st.subheader(translate_text("Symptoms:", st.session_state['target_language']))
    symptoms = get_symptoms()
    st.subheader(translate_text("Triggers:", st.session_state['target_language']))
    triggers = get_triggers()

    st.subheader(translate_text("Did something Help against the attack?", st.session_state['target_language']))
    help_response = st.text_area(translate_text("Write your response here", st.session_state['target_language']), height=100)

    if st.button(translate_text("Save Entry", st.session_state['target_language'])):
        new_entry = {
            'Date': date_selected,
            'Time': [entry['time'] for entry in st.session_state.time_severity_entries],
            'Severity': [entry['severity'] for entry in st.session_state.time_severity_entries],
            'Symptoms': symptoms,
            'Triggers': triggers,
            'Help': help_response
        }
        new_entry_df = pd.DataFrame([new_entry])
        st.session_state.data = pd.concat([st.session_state.data, new_entry_df], ignore_index=True)
        st.session_state.github.write_df(data_file, st.session_state.data, "added new entry")
        st.success(translate_text("Entry saved successfully!", st.session_state['target_language']))
        st.session_state.time_severity_entries = []

    st.subheader(translate_text("Saved Entries", st.session_state['target_language']))
    st.write(st.session_state.data)

def get_symptoms():
    symptoms = []
    col1, col2 = st.columns(2)
    with col1:
        symptoms.append(st.checkbox(translate_text("Anxiety", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Chest Pain", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Chills", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Chocking", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Cold", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Cold Hands", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Dizziness", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Feeling of danger", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Feeling of dread", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Heart racing", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Hot flushes", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Irrational thinking", st.session_state['target_language'])))
    with col2:
        symptoms.append(st.checkbox(translate_text("Nausea", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Nervousness", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Numb Hands", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Numbness", st.session_state['target_language'])))
        symptoms.append(st.checkbox(translate_text("Palpitations", st.session_state['target_language'])))
       
