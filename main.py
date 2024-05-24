import streamlit as st
from github_contents import GithubContents

github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"])

def show():
    st.title("Main Page")

def main_page():
    st.image("Logo.jpeg", width=600)
    
    # Sprachauswahl
    language = st.selectbox("Select Language", ["English", "Deutsch"])
    
    if language == "English":
        st.subheader("Anxiety Tracker Journal")
        st.write("""
            Welcome to FeelNow, your anxiety attack journal.
            This app helps you track and manage your anxiety by providing a platform to journal your thoughts 
            and feelings during anxiety attacks.
            
            ## What is FeelNow
            FeelNow is an app with which you can easily assess and monitor an acute panic attack. It is just like a diary and helps you to keep an eye on your mental health.
            
            ## What can the App do
            The app is supposed to help you write down important parts of a panic attack or even simply for your anxiety. It simplifies taking notes while feeling distressed by having the option to just choose how you're feeling instead of having to write your feelings down yourself.
            
            ## How do I use it
            You can create your own login by registering. You will then have a list of important points to assess during an acute attack, such as symptoms, possible triggers, who helped you at that moment or how strongly you felt them. If you do not feel like you're having a panic attack but you do feel anxious, you can do the same in the simpler version.
            """)
    elif language == "Deutsch":
        st.subheader("Angsttagebuch")
        st.write("""
            Willkommen bei FeelNow, deinem Angsttagebuch.
            Diese App hilft dir, deine Angst zu verfolgen und zu bewältigen, indem sie eine Plattform bietet, um deine Gedanken und Gefühle während Angstattacken zu protokollieren.
            
            ## Was ist FeelNow
            FeelNow ist eine App, mit der du leicht eine akute Panikattacke beurteilen und überwachen kannst. Es ist wie ein Tagebuch und hilft dir, deine psychische Gesundheit im Auge zu behalten.
            
            ## Was kann die App
            Die App soll dir helfen, wichtige Teile einer Panikattacke oder auch einfach nur deiner Angst aufzuschreiben. Sie vereinfacht das Notieren während du dich gestresst fühlst, indem sie die Möglichkeit bietet, einfach auszuwählen, wie du dich fühlst, anstatt deine Gefühle selbst aufschreiben zu müssen.
            
            ## Wie benutze ich sie
            Du kannst dein eigenes Login erstellen, indem du dich registrierst. Du hast dann eine Liste von wichtigen Punkten, die du während einer akuten Attacke beurteilen kannst, wie Symptome, mögliche Auslöser, wer dir in diesem Moment geholfen hat oder wie stark du sie empfunden hast. Wenn du das Gefühl hast, keine Panikattacke zu haben, aber dich ängstlich fühlst, kannst du dasselbe in der einfacheren Version tun.
            """)
    
    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("Login/Register"):
            switch_page("pages/login.py")

def switch_page(page_name):
    st.success("Redirecting to {} page...".format(page_name))
    # Hier können Sie die Logik hinzufügen, um zur angegebenen Seite zu navigieren

if __name__ == "__main__":
    main_page()
