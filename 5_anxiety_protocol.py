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

def translate_text(text, target_language):
    """Translate text using the deep_translator library."""
    translator = GoogleTranslator(target=target_language)
    translation = translator.translate(text)
    return translation

def main():
    init_github()
    init_credentials()

    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False

    # Language selection
    if 'target_language' not in st.session_state:
        languages = {
            "English": "en",
            "German": "de",
        }
        selected_language = st.selectbox("Choose your language", list(languages.keys()), index=0)
        st.session_state['target_language'] = languages[selected_language]
    else:
        st.write(translate_text("Language: ", st.session_state['target_language']) + st.session_state['target_language'])

    if not st.session_state['authentication']:
        options = st.sidebar.selectbox(translate_text("Select a page", st.session_state['target_language']), [translate_text("Login", st.session_state['target_language']), translate_text("Register", st.session_state['target_language'])])
        if options == translate_text("Login", st.session_state['target_language']):
            login_page()
        elif options == translate_text("Register", st.session_state['target_language']):
            register_page()
    else:
        st.sidebar.write(translate_text("Logged in as", st.session_state['target_language']) + f" {st.session_state['username']}")
        anxiety_protocol()

        logout_button = st.sidebar.button(translate_text("Logout", st.session_state['target_language']))
        if logout_button:
            st.session_state['authentication'] = False
            st.session_state.pop('username', None)
            switch_page("main.py")
            st.experimental_rerun()

def anxiety_protocol():
    username = st.session_state['username']
    data_file = f"{username}_anxiety_protocol_data.csv"
    
    if 'anxiety_data' not in st.session_state:
        if st.session_state.github.file_exists(data_file):
            st.session_state.anxiety_data = st.session_state.github.read_df(data_file)
        else:
            st.session_state.anxiety_data = pd.DataFrame(columns=['Date', 'Location', 'Anxiety Description', 'Cause', 'Triggers', 'Symptoms', 'Help'])

    st.title(translate_text("Anxiety Protocol", st.session_state['target_language']))

    # Question 1: Date
    date_selected = st.date_input(translate_text("Date", st.session_state['target_language']), value=datetime.date.today())

    # Question 2: Where are you
    st.subheader(translate_text("Where are you and what is the environment?", st.session_state['target_language']))
    location = st.text_area(translate_text("Write your response here", st.session_state['target_language']), key="location", height=100)
    
    st.subheader(translate_text("Try to describe your anxiety right now?", st.session_state['target_language']))
    anxiety_description = st.text_area(translate_text("Write your response here", st.session_state['target_language']), key="anxiety_description", height=100)

    st.subheader(translate_text("What do you think could be the cause?", st.session_state['target_language']))
    cause = st.text_area(translate_text("Write your response here", st.session_state['target_language']), key="cause", height=100)
    
    st.subheader(translate_text("Any specific triggers? For example Stress, Caffeine, Lack of Sleep, Social Event, Reminder of traumatic event", st.session_state['target_language']))
    triggers = st.text_area(translate_text("Write your response here", st.session_state['target_language']), key="triggers", height=100)

    # Question 3: Symptoms
    st.subheader(translate_text("Symptoms:", st.session_state['target_language']))
    symptoms_list = []
    col1, col2 = st.columns(2)
    with col1:
        if st.checkbox(translate_text("Chest Pain", st.session_state['target_language'])): symptoms_list.append("Chest Pain")
        if st.checkbox(translate_text("Chills", st.session_state['target_language'])): symptoms_list.append("Chills")
        if st.checkbox(translate_text("Cold", st.session_state['target_language'])): symptoms_list.append("Cold")
        if st.checkbox(translate_text("Cold Hands", st.session_state['target_language'])): symptoms_list.append("Cold Hands")
        if st.checkbox(translate_text("Dizziness", st.session_state['target_language'])): symptoms_list.append("Dizziness")
        if st.checkbox(translate_text("Feeling of danger", st.session_state['target_language'])): symptoms_list.append("Feeling of danger")
        if st.checkbox(translate_text("Heart racing", st.session_state['target_language'])): symptoms_list.append("Heart racing")
        if st.checkbox(translate_text("Hot flushes", st.session_state['target_language'])): symptoms_list.append("Hot flushes")
        if st.checkbox(translate_text("Nausea", st.session_state['target_language'])): symptoms_list.append("Nausea")
        if st.checkbox(translate_text("Nervousness", st.session_state['target_language'])): symptoms_list.append("Nervousness")
    with col2:
        if st.checkbox(translate_text("Numb Hands", st.session_state['target_language'])): symptoms_list.append("Numb Hands")
        if st.checkbox(translate_text("Numbness", st.session_state['target_language'])): symptoms_list.append("Numbness")
        if st.checkbox(translate_text("Shortness of Breath", st.session_state['target_language'])): symptoms_list.append("Shortness of Breath")
        if st.checkbox(translate_text("Sweating", st.session_state['target_language'])): symptoms_list.append("Sweating")
        if st.checkbox(translate_text("Tense Muscles", st.session_state['target_language'])): symptoms_list.append("Tense Muscles")
        if st.checkbox(translate_text("Tingly Hands", st.session_state['target_language'])): symptoms_list.append("Tingly Hands")
        if st.checkbox(translate_text("Trembling", st.session_state['target_language'])): symptoms_list.append("Trembling")
        if st.checkbox(translate_text("Tremor", st.session_state['target_language'])): symptoms_list.append("Tremor")
        if st.checkbox(translate_text("Weakness", st.session_state['target_language'])): symptoms_list.append("Weakness")

    # Display existing symptoms
    if 'symptoms' not in st.session_state:
        st.session_state.symptoms = []

    for symptom in st.session_state.symptoms:
        st.write(symptom)

    new_symptom = st.text_input(translate_text("Add new symptom:", st.session_state['target_language']), key="new_symptom")
    if st.button(translate_text("Add Symptom", st.session_state['target_language'])) and new_symptom:
        st.session_state.symptoms.append(new_symptom)

    # Question 5: Did something Help against the attack?
    st.subheader(translate_text("Did something Help against the Anxiety?", st.session_state['target_language']))
    help_response = st.text_area(translate_text("Write your response here", st.session_state['target_language']), key="help_response", height=100)

    if st.button(translate_text("Save Entry", st.session_state['target_language'])):
        new_entry = {
            'Date': date_selected,
            'Location': location,
            'Anxiety Description': anxiety_description,
            'Cause': cause,
            'Triggers': triggers,
            'Symptoms': ", ".join(symptoms_list),
            'Help': help_response
        }
        st.switch_page("pages/2_profile.py")
        new_entry_df = pd.DataFrame([new_entry])

        st.session_state.anxiety_data = pd.concat([st.session_state.anxiety_data, new_entry_df], ignore_index=True)

        st.session_state.github.write_df(data_file, st.session_state.anxiety_data, "added new entry")
        st.success(translate_text("Entry saved successfully!", st.session_state['target_language']))

    # Display saved entries
    st.subheader(translate_text("Saved Entries", st.session_state['target_language']))
    st.write(st.session_state.anxiety_data)

def add_time_severity():
    if 'time_severity_entries' not in st.session_state:
        st.session_state.time_severity_entries = []

    st.subheader(translate_text("Time & Severity", st.session_state['target_language']))

    # Display the current time
    current_time = datetime.datetime.now(pytz.timezone('Europe/Zurich')).strftime('%H:%M')
    st.write(translate_text(f"Current Time: {current_time}", st.session_state['target_language']))

    # Button to add a new time-severity entry
    with st.form(key='severity_form'):
        severity = st.slider(translate_text("Severity (1-10)", st.session_state['target_language']), min_value=1, max_value=10, key=f"severity_slider")
        if st.form_submit_button(translate_text("Add Severity", st.session_state['target_language'])):
            new_entry = {
                'time': current_time,
                'severity': severity
            }
            st.session_state.time_severity_entries.append(new_entry)
            st.success(translate_text(f"Added entry: Time: {current_time}, Severity: {severity}", st.session_state['target_language']))

    # Display all time-severity entries
    for entry in st.session_state.time_severity_entries:
        st.write(translate_text(f"Time: {entry['time']}, Severity: {entry['severity']}", st.session_state['target_language']))

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])
        print("github initialized")
    
def init_credentials():
    """Initialize or load the dataframe."""
    if 'df_users' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE):
            st.session_state.df_users = st.session_state.github.read_df(DATA_FILE)
        else:
            st.session_state.df_users = pd.DataFrame(columns=DATA_COLUMNS)

def login_page():
    """Login an existing user."""
    st.title(translate_text("Login", st.session_state['target_language']))
    with st.form(key='login_form'):
        username = st.text_input(translate_text("Username", st.session_state['target_language']))
        password = st.text_input(translate_text("Password", st.session_state['target_language']), type="password")
        if st.form_submit_button(translate_text("Login", st.session_state['target_language'])):
            authenticate(username, password)

def register_page():
    """Register a new user."""
    st.title(translate_text("Register", st.session_state['target_language']))
    with st.form(key='register_form'):
        new_username = st.text_input(translate_text("New Username", st.session_state['target_language']))
        new_name = st.text_input(translate_text("Name", st.session_state['target_language']))
        new_password = st.text_input(translate_text("New Password", st.session_state['target_language']), type="password")
        if st.form_submit_button(translate_text("Register", st.session_state['target_language'])):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())  # Hash the password
            hashed_password_hex = binascii.hexlify(hashed_password).decode()  # Convert hash to hexadecimal string
            
            # Check if the username already exists
            if new_username in st.session_state.df_users['username'].values:
                st.error(translate_text("Username already exists. Please choose a different one.", st.session_state['target_language']))
                return
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                # Writes the updated dataframe to GitHub data repository
                st.session_state.github.write_df(DATA_FILE, st.session_state.df_users, "added new user")
                st.success(translate_text("Registration successful! You can now log in.", st.session_state['target_language']))

def authenticate(username, password):
    """
    Authenticate the user.

    Parameters:
    username (str): The username to authenticate.
    password (str): The password to authenticate.
    """
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)

    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)  # Convert hex to bytes
        
        # Check the input password
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['authentication'] = True
            st.session_state['username'] = username
            st.success(translate_text('Login successful', st.session_state['target_language']))
            st.experimental_rerun()
        else:
            st.error(translate_text('Incorrect password', st.session_state['target_language']))
    else:
        st.error(translate_text('Username not found', st.session_state['target_language']))

def switch_page(page_name):
    st.success(translate_text(f"Redirecting to {page_name.replace('_', ' ')} page...", st.session_state['target_language']))
    time.sleep(3)
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
