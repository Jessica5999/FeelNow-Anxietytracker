import streamlit as st
from googletrans import Translator
from github_contents import GithubContents

# Initialize the GithubContents instance
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"]
)

# Initialize the Translator
translator = Translator()

# Dictionary to hold translations
translations = {
    "en": {
        "title": "Main Page",
        "subtitle": "Anxiety Tracker Journal",
        "welcome_text": """
            Welcome to FeelNow, your anxiety attack journal.
            This app helps you track and manage your anxiety by providing a platform to journal your thoughts 
            and feelings during anxiety attacks.
        """,
        "what_is_feelnow": "What is FeelNow",
        "feelnow_description": """
            FeelNow is an app with which you can easily assess and monitor an acute panic attack. It is just like a diary and helps you to keep an eye on your mental health.
        """,
        "app_capabilities": "What can the App do",
        "app_capabilities_description": """
            The app is supposed to help you write down important parts of a panic attack or even simply for your anxiety. It simplifies taking notes while feeling distressed by having the option to just choose how you're feeling instead of having to write your feelings down yourself.
        """,
        "how_to_use": "How do I use it",
        "how_to_use_description": """
            You can create your own login by registering. You will then have a list of important points to assess during an acute attack, such as symptoms, possible triggers, who helped you at that moment or how strongly you felt them. If you do not feel like you're having a panic attack but you do feel anxious, you can do the same in the simpler version.
        """,
        "login_button": "Login/Register"
    }
}

# List of supported languages
languages = {
    "en": "English",
    "de": "German",
    # Add more languages as needed
}

# Function to translate text
def translate_text(text, src, dest):
    try:
        translated = translator.translate(text, src=src, dest=dest)
        return translated.text
    except Exception as e:
        st.error(f"Error translating text: {e}")
        return text

# Function to get translated text
def get_translation(key, lang):
    if lang in translations and key in translations[lang]:
        return translations[lang][key]
    else:
        return translations["en"][key]  # Default to English

# Function to load translations
def load_translations():
    for lang in languages.keys():
        if lang != "en":
            for key in translations["en"].keys():
                translations[lang] = translations.get(lang, {})
                translations[lang][key] = translate_text(translations["en"][key], src="en", dest=lang)

# Load translations at startup
load_translations()

def main_page(lang):
    st.image("Logo.jpeg", width=600)
    st.subheader(get_translation("subtitle", lang))
    st.write(get_translation("welcome_text", lang))
    st.header(get_translation("what_is_feelnow", lang))
    st.write(get_translation("feelnow_description", lang))
    st.header(get_translation("app_capabilities", lang))
    st.write(get_translation("app_capabilities_description", lang))
    st.header(get_translation("how_to_use", lang))
    st.write(get_translation("how_to_use_description", lang))

    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button(get_translation("login_button", lang)):
            st.success(get_translation("login_button", lang))

# Main function
def main():
    st.sidebar.title("Language Selection")
    lang = st.sidebar.selectbox("Choose Language", options=list(languages.keys()), format_func=lambda x: languages[x])

    main_page(lang)

if __name__ == "__main__":
    main()
