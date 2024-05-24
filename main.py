import streamlit as st
from google.cloud import translate_v2 as translate

# Initialize the Google Cloud Translator
translate_client = translate.Client()

# Function to translate text
def translate_text(text, dest_language):
    if dest_language == "en":
        return text
    try:
        result = translate_client.translate(text, target_language=dest_language)
        return result['translatedText']
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text

# Function to show main page with dynamic content
def show_main_page(language):
    st.image("Logo.jpeg", width=600)
    st.subheader(translate_text("Anxiety Tracker Journal", language))
    st.write(translate_text("""
        Welcome to FeelNow, your anxiety attack journal.
        This app helps you track and manage your anxiety by providing a platform to journal your thoughts 
        and feelings during anxiety attacks.
        
        ## What is FeelNow
        FeelNow is an app with which you can easily assess and monitor an acute panic attack. It is just like a diary and helps you to keep an eye on your mental health.
        
        ## What can the App do
        The app is supposed to help you write down important parts of a panic attack or even simply for your anxiety. It simplifies taking notes while feeling distressed by having the option to just choose how you're feeling instead of having to write your feelings down yourself.
        
        ## How do I use it
        You can create your own login by registering. You will then have a list of important points to assess during an acute attack, such as symptoms, possible triggers, who helped you at that moment or how strongly you felt them. If you do not feel like you're having a panic attack but you do feel anxious, you can do the same in the simpler version.
    """, language))

    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button(translate_text("Login/Register", language)):
            st.write("Redirecting to login/register page...")  # Placeholder for page switch logic

# Function to handle language selection
def select_language():
    language = st.selectbox(
        "Choose Language / Sprache wählen", 
        ["en", "de", "es", "fr", "it", "pt", "ru", "zh"]
    )
    st.session_state["language"] = language

# Main function
def main():
    # Initialize session state
    if "language" not in st.session_state:
        st.session_state["language"] = "en"

    # Language selection
    select_language()
    language = st.session_state["language"]

    # Show main page content based on selected language
    show_main_page(language)

if __name__ == "__main__":
    main()
