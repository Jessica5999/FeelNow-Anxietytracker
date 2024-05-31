import streamlit as st
import binascii
import bcrypt
import time
import pandas as pd
from github_contents import GithubContents
from PIL import Image
from deep_translator import GoogleTranslator

# Constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'password']

def translate_text(text, target_language):
    """Translate text using the deep_translator library."""
    translator = GoogleTranslator(target=target_language)
    translation = translator.translate(text)
    return translation

def main_page():
    st.image("Logo.jpeg", width=600)
    st.title(translate_text("Your Anxiety Tracker Journal", st.session_state['target_language']))
    st.subheader(translate_text("Profile", st.session_state['target_language']))
    
    if 'username' in st.session_state:
        username = st.session_state['username']
        
        # Load user data
        user_data = st.session_state.df_users.loc[st.session_state.df_users['username'] == username]
        
        if not user_data.empty:
            st.write(translate_text("Username:", st.session_state['target_language']), username)
            st.write(translate_text("Name:", st.session_state['target_language']), user_data['name'].iloc[0])
        else:
            st.error(translate_text("User data not found.", st.session_state['target_language']))
    else:
        st.error(translate_text("User not logged in.", st.session_state['target_language']))
        if st.button(translate_text("Login/Register", st.session_state['target_language'])):
            switch_page("pages/1_login.py")

def anxiety_assessment():
    st.subheader(translate_text("Anxiety Assessment:", st.session_state['target_language']))
    st.write(translate_text("Do you feel like you're having an Anxiety Attack right now?", st.session_state['target_language']))
    if st.button(translate_text("Yes", st.session_state['target_language'])):
        switch_page("pages/4_anxiety_attack_protocol.py")
    if st.button(translate_text("No", st.session_state['target_language'])):
        anxiety_assessment2()

def anxiety_assessment2():
    st.write(translate_text("Are you anxious right now?", st.session_state['target_language']))
    if st.button(translate_text("Yes", st.session_state['target_language'])):
        switch_page("pages/5_anxiety_protocol.py")
    elif st.button(translate_text("No", st.session_state['target_language'])):
        gif_url = "https://64.media.tumblr.com/28fad0005f6861c08f2c07697ff74aa4/tumblr_n4y0patw7Q1rn953bo1_500.gif"
        gif_html = f'<img src="{gif_url}" width="400" height="300">'
        st.markdown(gif_html, unsafe_allow_html=True)

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
    """ Login an existing user. """
    st.title(translate_text("Login", st.session_state['target_language']))
    with st.form(key='login_form'):
        username = st.text_input(translate_text("Username", st.session_state['target_language']))
        password = st.text_input(translate_text("Password", st.session_state['target_language']), type="password")
        if st.form_submit_button(translate_text("Login", st.session_state['target_language'])):
            authenticate(username, password)
            if st.session_state['authentication']:
                switch_page("pages/2_profile.py")

def register_page():
    """ Register a new user. """
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

def authenticate(username, password):
    """ Authenticate the user. """
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)

    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)
        
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['authentication'] = True
            st.session_state['username'] = username
            st.success(translate_text('Login successful', st.session_state['target_language']))
            st.experimental_rerun()
        else:
            st.error(translate_text('Incorrect password', st.session_state['target_language']))
    else:
        st.error(translate_text('Username not found', st.session_state['target_language']))

# Page switching function
def switch_page(page_name):
    st.success(translate_text(f"Redirecting to {page_name.replace('_', ' ')} page...", st.session_state['target_language']))
    st.experimental_set_query_params(page=page_name)
    time.sleep(3)
    st.experimental_rerun()

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
        st.sidebar.write(translate_text("Logged in as", st.session_state['target_language']) + f" {st.session_state['username']}")
        main_page()
        anxiety_assessment()
        if st.sidebar.button(translate_text("Logout", st.session_state['target_language'])):
            st.session_state['authentication'] = False
            st.session_state.pop('username', None)
            switch_page("main.py")

if __name__ == "__main__":
    main()
