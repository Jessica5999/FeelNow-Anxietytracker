import streamlit as st
from googletrans import Translator
from github_contents import GithubContents

# Setup GitHub contents
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"])

# Initialize Translator
translator = Translator()

# Define the main page content
def main_page(language):
    st.image("Logo.jpeg", width=600)
    st.subheader("Anxiety Tracker Journal")
    
    content = {
        "title": "Welcome to FeelNow, your anxiety attack journal.",
        "intro": """
            This app helps you track and manage your anxiety by providing a platform to journal your thoughts 
            and feelings during anxiety attacks.
        """,
        "what_is": """
            ## What is FeelNow
            FeelNow is an app with which you can easily assess and monitor an acute panic attack. It is just like a diary and helps you to keep an eye on your mental health.
        """,
        "app_features": """
            ## What can the App do
            The app is supposed to help you write down important parts of a panic attack or even simply for your anxiety. It simplifies taking notes while feeling distressed by having the option to just choose how you're feeling instead of having to write your feelings down yourself.
        """,
        "how_to_use": """
            ## How do I use it
            You can create your own login by registering. You will then have a list of important points to assess during an acute attack, such as symptoms, possible triggers, who helped you at that moment or how strongly you felt them. If you do not feel like you're having a panic attack but you do feel anxious, you can do the same in the simpler version.
        """
    }
    
    # Translate content if language is not English
    if language != "en":
        content = {key: translator.translate(text, dest=language).text for key, text in content.items()}
    
    # Display content
    st.write(content["title"])
    st.write(content["intro"])
    st.write(content["what_is"])
    st.write(content["app_features"])
    st.write(content["how_to_use"])

    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("Login/Register"):
            st.success("Redirecting to login page...")

# Sidebar for language selection
language = st.sidebar.selectbox("Select Language", ["en", "de", "es", "fr", "zh-cn"])

# Show main page with selected language
main_page(language)
