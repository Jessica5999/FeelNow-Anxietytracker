import streamlit as st
import pandas as pd
from github_contents import GithubContents
import time

# Initialize GitHubContents
def init_github():
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])
        print("github initialized")

# Translate text function
def translate_text(text, target_language):
    from deep_translator import GoogleTranslator
    translator = GoogleTranslator(target=target_language)
    return translator.translate(text)

def main_page():
    init_github()  # Initialize GitHubContents
    st.image("Logo.jpeg", width=600)
    st.title("Your Anxiety Tracker Journal")
    st.subheader("Profile")

    target_language = st.session_state.get('target_language', 'en')

    if 'username' in st.session_state:
        username = st.session_state['username']
        
        # Load user data
        user_data = st.session_state.df_users.loc[st.session_state.df_users['username'] == username]
        
        if not user_data.empty:
            st.write(translate_text("Username:", target_language), username)
            st.write(translate_text("Name:", target_language), user_data['name'].iloc[0])
            st.write(translate_text("Birthday:", target_language), user_data['birthday'].iloc[0])
        else:
            st.error(translate_text("User data not found.", target_language))
    else:
        st.error(translate_text("User not logged in.", target_language))
        if st.button(translate_text("Login/Register", target_language)):
            switch_page("pages/1_login.py")

def init_credentials():
    if 'df_users' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE):
            st.session_state.df_users = st.session_state.github.read_df(DATA_FILE)
        else:
            st.session_state.df_users = pd.DataFrame(columns=DATA_COLUMNS)

def switch_page(page_name):
    st.success(f"Redirecting to {page_name.replace('_', ' ')} page...")
    time.sleep(3)
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

if __name__ == "__main__":
    init_github()
    init_credentials()
    main_page()
