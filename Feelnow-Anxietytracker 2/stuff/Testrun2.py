from github_contents import GithubContents
import streamlit as st
from PIL import Image 
import pandas as pd
import datetime

def main_page():
    st.markdown( f"""
        <h1 style='font-size: 4em; text-align: '>FeelNow</h1>
        """,
        unsafe_allow_html=True
    )
    st.image("Logo.png", width=400)  # Adapted logo size
    st.subheader("Anxiety Tracker Journal")
    st.write("""
        Welcome to FeelNow, your anxiety attack journal.
        This app helps you track and manage your anxiety by providing a platform to journal your thoughts 
        and feelings during anxiety attacks.
        
        ## What is FeelNow
        (Description of the app)
        
        ## What can the App do
        (Features and functionalities)
        
        ## How do I use it
        (Instructions on how to use the app)
        """)

    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("Login/Register"):
            # Redirect to login/register page
            st.write("Redirecting to login/register page...")
            # Add redirection logic here

if __name__ == "__main__":
    main_page()

# Hier könntest du auch andere Streamlit-Komponenten verwenden, um das Design anzupassen
def main():
    st.title('Feelnow - Anxietytracker')

    # Hier könnten die Optionen für Login oder Registrieren angezeigt werden
    option = st.sidebar.selectbox('Choose an option:', ['Login', 'Register'])

    if option == 'Login':
        login()
    elif option == 'Register':
        register()

def login():
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        # Hier könntest du den Login-Prozess implementieren
        st.success('Logged in successfully!')

def register():
    st.subheader('Register')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Register'):
        # Hier könntest du den Registrierungsprozess implementieren
        st.success('Registered successfully!')

if __name__ == "__main__":
    main()

def anxiety_attack_protocol():
    st.write("Redirecting to Anxiety Attack Protocol page...")  # (anxietyattack-protocol)

def redirect_question_2():
    st.write("Are you anxious right now?")

def anxiety_protocol():
    st.write("Redirecting to Anxiety Protocol page...")  # (anxiety-protocol)

def No_2_question():
    st.experimental_rerun()

def main_page():
    st.title("FeelNow")
    st.image("Logo.jpg", width=150)  # Logo on the left upper corner
    st.write("---")
    
    st.write("Anxiety Assessment:")
    
    st.write("Do you feel like you're having an Anxiety Attack right now?")
    if st.button("Yes"):
        anxiety_attack_protocol()
    elif st.button("No"):
        redirect_question_2()
        if st.button("Yes "):
            anxiety_protocol()
        elif st.button("No "):
            No_2_question()

if __name__ == "__main__":
    main_page()

def anxiety_attack_protocol():
    # Check if the session state object exists, if not, initialize it
    if 'button_count' not in st.session_state:
        st.session_state.button_count = 0
        st.session_state.times = []
        st.session_state.severities = []

    st.write("Anxiety Attack Protocol Page")

    # Question 1: Date
    date_selected = st.date_input("Date", value=datetime.date.today())

    # Question 2: Time & Severity
    add_time_severity()

    # Question 3: Symptoms
    st.subheader("Symptoms:")
    col1, col2 = st.columns(2)
    with col1:
        symptoms_anxiety = st.checkbox("Anxiety")
        symptoms_chestpain = st.checkbox("Chest Pain")
        symptoms_chills = st.checkbox("Chills")
        symptoms_chocking = st.checkbox("Chocking")
        symptoms_cold = st.checkbox("Cold")
        symptoms_coldhands = st.checkbox("Cold Hands")
        symptoms_dizziness = st.checkbox("Dizziness")
        symptoms_feelingdanger = st.checkbox("Feeling of danger")
        symptoms_feelingdread = st.checkbox("Feeling of dread")
        symptoms_heartracing = st.checkbox("Heart racing")
        symptoms_hotflushes = st.checkbox("Hot flushes")
        symptoms_irrationalthinking = st.checkbox("Irrational thinking")
    with col2:
        symptoms_nausea = st.checkbox("Nausea")
        symptoms_nervous = st.checkbox("Nervousness")
        symptoms_numbhands = st.checkbox("Numb Hands")
        symptoms_numbness = st.checkbox("Numbness")
        symptoms_palpitations = st.checkbox("Palpitations")
        symptoms_shortbreath = st.checkbox("Shortness of Breath")
        symptoms_sweating = st.checkbox("Sweating")
        symptoms_tensemuscles = st.checkbox("Tense Muscles")
        symptoms_tinglyhands = st.checkbox("Tingly Hands")
        symptoms_trembling = st.checkbox("Trembling")
        symptoms_tremor = st.checkbox("Tremor")
        symptoms_weakness = st.checkbox("Weakness")
    if 'symptoms' not in st.session_state:
        st.session_state.symptoms = []

    # Display existing symptoms
    for symptom in st.session_state.symptoms:
        st.write(symptom)

    new_symptom = st.text_input("Add new symptom:")
    if st.button("Add Symptom") and new_symptom:
        st.session_state.symptoms.append(new_symptom)

    # Question 4: Triggers
    st.subheader("Triggers:")
    triggers = st.multiselect("Select Triggers", ["Stress", "Caffeine", "Lack of Sleep", "Social Event", "Reminder of traumatic event", "Alcohol", "Conflict", "Family problems"])
    if 'triggers' not in st.session_state:
        st.session_state.triggers = []

    new_trigger = st.text_input("Add new trigger:")
    if st.button("Add Trigger") and new_trigger:
        st.session_state.triggers.append(new_trigger)

    for trigger in st.session_state.triggers:
        st.write(trigger)

    # Question 5: Did something Help against the attack?
    st.subheader("Did something Help against the attack?")
    help_response = st.text_area("Write your response here", height=100)

def add_time_severity():
    st.subheader("Time & Severity")
    
    # Initialize times list if not already initialized
    if 'times' not in st.session_state:
        st.session_state.times = []

    for i in range(st.session_state.button_count + 1):
        if i < len(st.session_state.times):
            time_selected, severity = st.session_state.times[i]
        else:
            time_selected = datetime.datetime.now().time()
            severity = 1

        # Convert time_selected to string with minute precision
        time_selected_str = time_selected.strftime('%H:%M')
        
        # Display time input with minute precision
        time_selected_str = st.text_input(f"Time {i+1}", value=time_selected_str)
        
        # Convert the string back to datetime.time object
        time_selected = datetime.datetime.strptime(time_selected_str, '%H:%M').time()
        
        severity = st.slider(f"Severity (1-10) {i+1}", min_value=1, max_value=10, value=severity)
        
        # Update time and severity in session state
        if len(st.session_state.times) <= i:
            st.session_state.times.append((time_selected, severity))
        else:
            st.session_state.times[i] = (time_selected, severity)

    if st.button("Add Time & Severity"):
        st.session_state.button_count += 1

def main_page():
    st.title("FeelNow")
    anxiety_attack_protocol()

if __name__ == "__main__":
    main_page()


def anxiety_protocol():
    # Check if the session state object exists, if not, initialize it
    if 'button_count' not in st.session_state:
        st.session_state.button_count = 0
        st.session_state.times = []
        st.session_state.severities = []

    st.write("Anxiety Protocol Page")

    # Question 1: Date
    date_selected = st.date_input("Date", value=datetime.date.today())

    # Question 2: Where are you
    st.subheader("Where are you and what is the environment?")
    help_response = st.text_area("Write your response here", key="location", height=100)
    
    st.subheader("Try to describe your anxiety right now?")
    help_response = st.text_area("Write your response here", key="anxiety_description", height=100)

    st.subheader("What do you think could be the cause?")
    help_response = st.text_area("Write your response here", key="cause", height=100)
    
    st.subheader("Any specific triggers? For example Stress, Caffeine, Lack of Sleep, Social Event, Reminder of traumatic event")
    help_response = st.text_area("Write your response here", key="triggers", height=100)

    # Question 3: Symptoms
    st.subheader("Symptoms:")
    col1, col2 = st.columns(2)
    with col1:
        symptoms_chestpain = st.checkbox("Chest Pain")
        symptoms_chills = st.checkbox("Chills")
        symptoms_cold = st.checkbox("Cold")
        symptoms_coldhands = st.checkbox("Cold Hands")
        symptoms_dizziness = st.checkbox("Dizziness")
        symptoms_feelingdanger = st.checkbox("Feeling of danger")
        symptoms_heartracing = st.checkbox("Heart racing")
        symptoms_hotflushes = st.checkbox("Hot flushes")
    with col2:
        symptoms_nausea = st.checkbox("Nausea")
        symptoms_nervous = st.checkbox("Nervousness")
        symptoms_numbhands = st.checkbox("Numb Hands")
        symptoms_numbness = st.checkbox("Numbness")
        symptoms_shortbreath = st.checkbox("Shortness of Breath")
        symptoms_sweating = st.checkbox("Sweating")
        symptoms_tensemuscles = st.checkbox("Tense Muscles")
        symptoms_tinglyhands = st.checkbox("Tingly Hands")
        symptoms_trembling = st.checkbox("Trembling")
        symptoms_tremor = st.checkbox("Tremor")
        symptoms_weakness = st.checkbox("Weakness")
    if 'symptoms' not in st.session_state:
        st.session_state.symptoms = []

    # Display existing symptoms
    for symptom in st.session_state.symptoms:
        st.write(symptom)

    new_symptom = st.text_input("Add new symptom:", key="new_symptom")
    if st.button("Add Symptom") and new_symptom:
        st.session_state.symptoms.append(new_symptom)

    # Question 5: Did something Help against the attack?
    st.subheader("Did something Help against the Anxiety?")
    help_response = st.text_area("Write your response here", key="help_response", height=100)

def main_page():
    st.title("FeelNow")
    anxiety_protocol()

if __name__ == "__main__":
    main_page()