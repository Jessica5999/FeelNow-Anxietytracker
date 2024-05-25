import streamlit as st
from github_contents import GithubContents
from googletrans import Translator

github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"])

translator = Translator()

def translate_text(text, target_language):
    translation = translator.translate(text, dest=target_language)
    return translation.text

def show():
    st.title("Main Page")

def main_page():
    col1, col2, col3 = st.columns([0.7, 0.05, 0.25])
    with col1:
        st.image("Logo.jpeg", width=600)
    with col3:
        languages = {
            "English": "en",
            "German": "de",
            "Spanish": "es",
            "French": "fr",
            "Chinese": "zh-cn"
        }
        selected_language = st.selectbox("Select Language", list(languages.keys()))
        target_language = languages[selected_language]

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

    translated_text = translate_text(original_text, target_language)
    st.write(translated_text)

    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("Login/Register"):
            st.switch_page("pages/login.py")

def switch_page(page_name):
    st.success("Redirecting to {} page...".format(page_name))
    # Hier können Sie die Logik hinzufügen, um zur angegebenen Seite zu navigieren

if __name__ == "__main__":
    main_page()
