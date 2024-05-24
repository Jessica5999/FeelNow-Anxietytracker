import streamlit as st
from github_contents import GithubContents

github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"])

# Dictionary for language translations
translations = {
    "en": {
        "title": "Main Page",
        "subheader": "Anxiety Tracker Journal",
        "welcome": """
            Welcome to FeelNow, your anxiety attack journal.
            This app helps you track and manage your anxiety by providing a platform to journal your thoughts 
            and feelings during anxiety attacks.
            """,
        "what_is": "## What is FeelNow",
        "what_is_text": """
            FeelNow is an app with which you can easily assess and monitor an acute panic attack. It is just like a diary and helps you to keep an eye on your mental health.
            """,
        "what_can": "## What can the App do",
        "what_can_text": """
            The app is supposed to help you write down important parts of a panic attack or even simply for your anxiety. It simplifies taking notes while feeling distressed by having the option to just choose how you're feeling instead of having to write your feelings down yourself.
            """,
        "how_to": "## How do I use it",
        "how_to_text": """
            You can create your own login by registering. You will then have a list of important points to assess during an acute attack, such as symptoms, possible triggers, who helped you at that moment or how strongly you felt them. If you do not feel like you're having a panic attack but you do feel anxious, you can do the same in the simpler version.
            """,
        "login_register": "Login/Register"
    },
    "de": {
        "title": "Hauptseite",
        "subheader": "Angst-Tracker-Journal",
        "welcome": """
            Willkommen bei FeelNow, Ihrem Angstattacken-Tagebuch.
            Diese App hilft Ihnen, Ihre Angst zu verfolgen und zu bewältigen, indem sie eine Plattform bietet, um Ihre Gedanken und Gefühle während Angstattacken zu notieren.
            """,
        "what_is": "## Was ist FeelNow",
        "what_is_text": """
            FeelNow ist eine App, mit der Sie eine akute Panikattacke leicht beurteilen und überwachen können. Es ist wie ein Tagebuch und hilft Ihnen, Ihre psychische Gesundheit im Auge zu behalten.
            """,
        "what_can": "## Was kann die App tun",
        "what_can_text": """
            Die App soll Ihnen helfen, wichtige Teile einer Panikattacke oder einfach Ihre Angst aufzuschreiben. Es vereinfacht das Notieren während der Notlage, indem Sie einfach auswählen können, wie Sie sich fühlen, anstatt Ihre Gefühle selbst aufzuschreiben.
            """,
        "how_to": "## Wie benutze ich es",
        "how_to_text": """
            Sie können Ihr eigenes Login erstellen, indem Sie sich registrieren. Sie haben dann eine Liste wichtiger Punkte zur Bewertung während einer akuten Attacke, wie Symptome, mögliche Auslöser, wer Ihnen in diesem Moment geholfen hat oder wie stark Sie diese empfunden haben. Wenn Sie das Gefühl haben, keine Panikattacke zu haben, aber dennoch ängstlich sind, können Sie dasselbe in der einfacheren Version tun.
            """,
        "login_register": "Einloggen/Registrieren"
    }
}

# Language selection
language = st.sidebar.selectbox("Select Language", ("English", "Deutsch"))

# Map selected language to dictionary key
lang_key = "en" if language == "English" else "de"

def show():
    st.title(translations[lang_key]["title"])

def main_page():
    st.image("Logo.jpeg", width=600)
    st.subheader(translations[lang_key]["subheader"])
    st.write(translations[lang_key]["welcome"])
    st.write(translations[lang_key]["what_is"])
    st.write(translations[lang_key]["what_is_text"])
    st.write(translations[lang_key]["what_can"])
    st.write(translations[lang_key]["what_can_text"])
    st.write(translations[lang_key]["how_to"])
    st.write(translations[lang_key]["how_to_text"])

    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button(translations[lang_key]["login_register"]):
            st.success("Redirecting to login/register page...")
            switch_page("pages/login.py")

def switch_page(page_name):
    # Add logic to switch to the specified page
    st.success(f"Redirecting to {page_name} page...")

if __name__ == "__main__":
    main_page()
