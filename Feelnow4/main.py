import streamlit as st
from github_contents import GithubContents
from deep_translator import GoogleTranslator  # Import the GoogleTranslator class from the deep_translator library
import time  # Ensure that you import the time module

github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"])

def main_sidebar():
    st.sidebar.title("Navigation")
    profile = st.sidebar.checkbox("Profile")
    anxiety_attack = st.sidebar.checkbox("Anxiety Attack")
    anxiety = st.sidebar.checkbox("Anxiety")
    mainpage = st.sidebar.checkbox("Mainpage")

    if profile:
        switch_page("pages/2_profile.py")
    elif anxiety_attack:
        switch_page("pages/4_anxiety_attack_protocol.py")
    elif anxiety:
        switch_page("pages/5_anxiety_protocol.py")
    elif mainpage:
        switch_page("main.py")

# Function to translate text using the deep_translator library
def translate_text(text, target_language):
    translator = GoogleTranslator(target=target_language)  # Initialize the GoogleTranslator object
    translation = translator.translate(text)  # Translate the text
    return translation

# Function to display the main page
def main_page():
    st.image("Logo.jpeg", width=600)
    st.subheader("Anxiety Tracker Journal")

    # Supported languages
    languages = {
        "English": "en",
        "German": "de",
    }

    # Language selection
    selected_language = st.selectbox("Choose your language", list(languages.keys()), index=0)
    st.session_state['target_language'] = languages[selected_language]

    original_text = (
        "Welcome to FeelNow, your anxiety attack journal. "
        "This app helps you track and manage your anxiety by providing a platform to journal your thoughts "
        "and feelings during anxiety attacks.\n\n"
        "## What is FeelNow\n"
        "FeelNow is an app with which you can easily assess and monitor an acute panic attack. It is just like a diary and helps you to keep an eye on your mental health.\n\n"
        "## What can the App do\n"
        "The app is supposed to help you write down important parts of a panic attack or even simply for your anxiety. It simplifies taking notes while feeling distressed by having the option to just choose how you're feeling instead of having to write your feelings down yourself.\n\n"
        "## How do I use it\n"
        "You can create your own login by registering. You will then have a list of important points to assess during an acute attack, such as symptoms, possible triggers, who helped you at that moment or how strongly you felt them. If you do not feel like you're having a panic attack but you do feel anxious, you can do the same in the simpler version.\n"
    )

    # Translate the text
    translated_text = translate_text(original_text, st.session_state['target_language'])
    st.write(translated_text)

    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("Login/Register"):
            st.switch_page("pages/1_login.py")

def switch_page(page_name):
    st.success(f"Redirecting to {page_name.replace('_', ' ')} page...")
    time.sleep(3)
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

if __name__ == "__main__":
    main_page()