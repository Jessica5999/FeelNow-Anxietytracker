import streamlit as st
from github_contents import GithubContents
import requests

# Set up GitHub connection
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"])

# Function to translate text using DeepL API
def translate_text(text, target_language):
    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {st.secrets['deepl']['api_key']}"
    }
    data = {
        "text": text,
        "target_lang": target_language
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()["translations"][0]["text"]

# Sidebar for language selection
st.sidebar.title("Language Selection")
language = st.sidebar.selectbox("Choose language", ["EN", "DE", "FR", "ES", "IT", "NL"])

def show():
    st.title("Main Page")

def main_page():
    st.image("Logo.jpeg", width=600)
    st.subheader("Anxiety Tracker Journal")

    # Texts to translate
    texts = {
        "welcome": "Welcome to FeelNow, your anxiety attack journal. This app helps you track and manage your anxiety by providing a platform to journal your thoughts and feelings during anxiety attacks.",
        "what_is_feelnow": "FeelNow is an app with which you can easily assess and monitor an acute panic attack. It is just like a diary and helps you to keep an eye on your mental health.",
        "what_can_app_do": "The app is supposed to help you write down important parts of a panic attack or even simply for your anxiety. It simplifies taking notes while feeling distressed by having the option to just choose how you're feeling instead of having to write your feelings down yourself.",
        "how_to_use": "You can create your own login by registering. You will then have a list of important points to assess during an acute attack, such as symptoms, possible triggers, who helped you at that moment or how strongly you felt them. If you do not feel like you're having a panic attack but you do feel anxious, you can do the same in the simpler version."
    }

    # Translate texts
    translated_texts = {key: translate_text(text, language) for key, text in texts.items()}

    st.write(translated_texts["welcome"])
    st.write("## What is FeelNow")
    st.write(translated_texts["what_is_feelnow"])
    st.write("## What can the App do")
    st.write(translated_texts["what_can_app_do"])
    st.write("## How do I use it")
    st.write(translated_texts["how_to_use"])

    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("Login/Register"):
            st.switch_page("pages/login.py")

def switch_page(page_name):
    st.success("Redirecting to {} page...".format(page_name))
    # Hier können Sie die Logik hinzufügen, um zur angegebenen Seite zu navigieren

if __name__ == "__main__":
    main_page()
