import streamlit as st
import bcrypt
import binascii
import datetime
from github_contents import GithubContents
import pandas as pd
from deep_translator import GoogleTranslator
import time

# Constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'birthday', 'password']

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

def translate_text(text, target_language):
    """Translate text using the deep_translator library."""
    translator = GoogleTranslator(target=target_language)
    translation = translator.translate(text)
    return translation

def register_page():
    """ Register a new user. """
    st.title(translate_text("Register", st.session_state['target_language']))
    with st.form(key='register_form'):
        st.write(translate_text("Please fill in the following details:", st.session_state['target_language']))
        new_first_name = st.text_input(translate_text("First Name", st.session_state['target_language']))
        new_last_name = st.text_input(translate_text("Last Name", st.session_state['target_language']))
        new_username = st.text_input(translate_text("Username", st.session_state['target_language']))
        new_birthday = st.date_input(translate_text("Birthday", st.session_state['target_language']), min_value=datetime.date(1900, 1, 1))
        new_password = st.text_input(translate_text("Password", st.session_state['target_language']), type="password")
        
        submit_button = st.form_submit_button(translate_text("Register", st.session_state['target_language']))
        
        if submit_button:
            if new_username in st.session_state.df_users['username'].values:
                st.error(translate_text("Username already exists. Please choose a different one.", st.session_state['target_language']))
                return
            else:
                # Hash the password
                hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
                hashed_password_hex = binascii.hexlify(hashed_password).decode()
                
                # Create a new user DataFrame
                new_user_data = [[new_username, f"{new_first_name} {new_last_name}", new_birthday, hashed_password_hex]]
                new_user = pd.DataFrame(new_user_data, columns=DATA_COLUMNS)
                
                # Concatenate the new user DataFrame with the existing one
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                # Write the updated dataframe to GitHub data repository
                try:
                    st.session_state.github.write_df(DATA_FILE, st.session_state.df_users, "added new user")
                    st.success(translate_text("Registration successful! You can now log in.", st.session_state['target_language']))
                    st.switch_page("pages/2_profile.py")
                except GithubContents.UnknownError as e:
                    st.error(translate_text(f"An unexpected error occurred: {e}", st.session_state['target_language']))
                except Exception as e:
                    st.error(translate_text(f"An unexpected error occurred: {e}", st.session_state['target_language']))

def login_page():
    """ Login an existing user. """
    st.image("Logo.jpeg", width=600)
    st.write("---")
    st.title(translate_text("Login", st.session_state['target_language']))
    with st.form(key='login_form'):
        username = st.text_input(translate_text("Username", st.session_state['target_language']))
        password = st.text_input(translate_text("Password", st.session_state['target_language']), type="password")
        if st.form_submit_button(translate_text("Login", st.session_state['target_language'])):
            authenticate(username, password)
            st.switch_page("pages/2_profile.py")

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
        
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['authentication'] = True
            st.session_state['username'] = username
            st.success(translate_text('Login successful', st.session_state['target_language']))
            st.switch_page("pages/2_profile.py")
            st.experimental_rerun()
        else:
            st.error(translate_text('Incorrect password', st.session_state['target_language']))
    else:
        st.error(translate_text('Username not found', st.session_state['target_language']))

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
        options = st.sidebar.selectbox(translate_text("Select a page", st.session_state['target_language']), ["Login", "Register"])
        if options == "Login":
            login_page()
        elif options == "Register":
            register_page()
    else:
        st.image("Logo.jpeg", width=600)
        st.write("---")
        st.write(translate_text("### You are already logged in", st.session_state['target_language']))
        st.sidebar.write(translate_text("Logged in as", st.session_state['target_language']) + f" {st.session_state['username']}")
        logout_button = st.button(translate_text("Logout", st.session_state['target_language']))
        if logout_button:
            st.session_state['authentication'] = False
            st.session_state.pop('username', None)
            st.experimental_rerun()

def switch_page(page_name):
    st.success(f"Redirecting to {page_name.replace('_', ' ')} page...")
    time.sleep(3)
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
