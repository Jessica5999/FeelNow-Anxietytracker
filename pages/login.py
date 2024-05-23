import binascii
import streamlit as st
import pandas as pd
import bcrypt
from github_contents import GithubContents

# Constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'password']

def show_login():
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(username, password)

def show_register():
    st.title("Register")
    with st.form(key='register_form'):
        new_username = st.text_input("New Username")
        new_name = st.text_input("Name")
        new_password = st.text_input("New Password", type="password")
        if st.form_submit_button("Register"):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
            hashed_password_hex = binascii.hexlify(hashed_password).decode()

            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose a different one.")
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                st.session_state.github.write_df(DATA_FILE, st.session_state.df_users, "added new user")
                st.success("Registration successful! You can now log in.")
                st.session_state['page'] = 'login'
                st.experimental_rerun()

def authenticate(username, password):
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)

    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)
        
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes):
            st.session_state['authentication'] = True
            st.session_state['username'] = username
            st.success('Login successful')
            st.session_state['page'] = 'attack'
            st.experimental_rerun()
        else:
            st.error('Incorrect password')
    else:
        st.error('Username not found')

def init_github():
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])

def init_credentials():
    if 'df_users' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE):
            st.session_state.df_users = st.session_state.github.read_df(DATA_FILE)
        else:
            st.session_state.df_users = pd.DataFrame(columns=DATA_COLUMNS)

def main():
    init_github()
    init_credentials()

    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False

    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'

    if st.session_state['authentication']:
        st.session_state['page'] = 'attack'

    page = st.session_state['page']

    if page == 'login':
        show_login()
    elif page == 'register':
        show_register()
    elif page == 'attack':
        st.experimental_set_query_params(page="attack")
        st.experimental_rerun()

    if not st.session_state['authentication']:
        options = st.sidebar.selectbox("Select a page", ["Login", "Register"])
        if options == "Login":
            st.session_state['page'] = 'login'
            st.experimental_rerun()
        elif options == "Register":
            st.session_state['page'] = 'register'
            st.experimental_rerun()

if __name__ == "__main__":
    main()
