import base64, json
import pandas as pd
from requests import Session
from io import StringIO
import streamlit as st
from github_contents import GithubContents

class AuthManager:
    def __init__(self):
        self.github_token = GithubContents(owner='owner', repo='repo', token='your_token')

    def register_user(self, username, password):
        user_data = {'username': username, 'password': password}
        self.github_token.write_json('user_data.json', user_data, 'User registration')

    def login_user(self, username, password):
        user_data = self.github_token.read_json('user_data.json')
        if user_data['username'] == username and user_data['password'] == password:
            return True
        else:
            return False

def main():
    auth_manager = AuthManager()
    st.title('Feelnow - Anxietytracker')
    option = st.sidebar.selectbox('Choose an option:', ['Login', 'Register'])

    if option == 'Login':
        login(auth_manager)
    elif option == 'Register':
        register(auth_manager)

def login(auth_manager):
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if auth_manager.login_user(username, password):
            st.success('Logged in successfully!')
        else:
            st.error('Invalid username or password.')

def register(auth_manager):
    st.subheader('Register')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Register'):
        auth_manager.register_user(username, password)
        st.success('Registered successfully!')

if __name__ == "__main__":
    main()
