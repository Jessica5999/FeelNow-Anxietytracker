import streamlit as st
from github_contents import GithubContents
from deep_translator import GoogleTranslator  # Import the GoogleTranslator class from the deep_translator library

# Initialize the GithubContents object
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"]
)

# Function to translate text using the deep_translator library
def translate_text(text, target_language):
    translator = GoogleTranslator(target=target_language)  # Initialize the GoogleTranslator object
    translation = translator.translate(text)  # Translate the text
    return translation

# Function to display the main page
def show():
    st.title("Main Page")

# Function to display the main page content
def main_page():
    st.image("Logo.jpeg", width=600)
    st.subheader("Anxiety Tracker Journal")

    # Supported languages
    languages = {
        "English": "en",
        "German": "de",
        "Spanish": "es",
        "French": "fr",
        "Chinese": "zh-cn"
    }

    # Language selection
    selected_language = st.selectbox("Select Language", list(languages.keys()))
    target_language = languages[selected_language]

    # Original text
    original_text = """
Welcome to FeelNow, your anxiety attack journal.
This app helps you track and manage your anxiety by providing a platform to journal your thoughts 
and feelings during anxiety attacks.

## What is FeelNow
FeelNow is an app with which you can easily assess and monitor an acute panic attack. It is just like a diary and helps you to keep an eye on your mental health.

## What can the App do
The app is supposed to help you write down important parts of a panic attack or even simply for your anxiety. It simplifies taking notes while feeling distressed by having the option to just choose how you're feeling instead of having to write your feelings down yourself.

## How do I use it
You can create your own login by registering. You will then have a list of important points to assess during an acute attack, such as symptoms, possible triggers, who helped you at that moment or how strongly you felt them. If you do not feel like you're having a panic attack but you do feel anxious, you can do the same in the simpler version.
    """

    # Translate the text
    translated_text = translate_text(original_text, target_language)
    st.write(translated_text)

    # Login/Register button
    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("Login/Register"):
            st.session_state.page = "login"

def switch_page(login.py):
    st.success("Redirecting to {login.py} ".format(login.py))
    # Hier können Sie die Logik hinzufügen, um zur angegebenen Seite zu navigieren

if __name__ == "__main__":
    main_page()
