import streamlit as st
import datetime
import pandas as pd
import bcrypt
import binascii
from github_contents import GithubContents
from pytz import timezone

# Constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'password']
ATTACK_DATA_FILE = "AttackData.csv"
ATTACK_DATA_COLUMNS = ['username', 'date', 'time_severity', 'symptoms', 'triggers', 'help_response']

# Set the time zone to Switzerland
swiss_tz = timezone('Europe/Zurich')

# Initialize session state variables
if 'authentication' not in st.session_state:
    st.session_state['authentication'] = False
    st.session_state['username'] = None

if 'times' not in st.session_state:
    st.session_state['times'] = []

if 'symptoms' not in st.session_state:
    st.session_state['symptoms'] = []

if 'triggers' not in st.session_state:
    st.session_state['triggers'] = []

if 'show_time_severity' not in st.session_state:
    st.session_state['show_time_severity'] = False

if 'button_count' not in st.session_state:
    st.session_state['button_count'] = 0

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"]
        )
        print("GitHub initialized")

def init_credentials():
    """Initialize or load the dataframe."""
    if 'df_users' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE):
            st.session_state.df_users = st.session_state.github.read_df(DATA_FILE)
        else:
            st.session_state.df_users = pd.DataFrame(columns=DATA_COLUMNS)

def authenticate(username, password):
    """Authenticate the user."""
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)

    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)  # Convert hex to bytes
        
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['authentication'] = True
            st.session_state['username'] = username
            st.success('Login successful')
            st.experimental_rerun()
        else:
            st.error('Incorrect password')
    else:
        st.error('Username not found')

def register_page():
    """Register a new user."""
    st.title("Register")
    with st.form(key='register_form'):
        new_username = st.text_input("New Username")
        new_name = st.text_input("Name")
        new_password = st.text_input("New Password", type="password")
        if st.form_submit_button("Register"):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())  # Hash the password
            hashed_password_hex = binascii.hexlify(hashed_password).decode()  # Convert hash to hexadecimal string
            
            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose a different one.")
                return
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                # Write the updated dataframe to GitHub data repository
                st.session_state.github.write_df(DATA_FILE, st.session_state.df_users, "Added new user")
                st.success("Registration successful! You can now log in.")

def login_page():
    """Login an existing user."""
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(username, password)

def save_to_csv(data):
    """Save data to CSV file."""
    attack_data_df = pd.DataFrame([data], columns=ATTACK_DATA_COLUMNS)
    if st.session_state.github.file_exists(ATTACK_DATA_FILE):
        existing_data = st.session_state.github.read_df(ATTACK_DATA_FILE)
        attack_data_df = pd.concat([existing_data, attack_data_df], ignore_index=True)
    st.session_state.github.write_df(ATTACK_DATA_FILE, attack_data_df, "Added new attack data")

def anxiety_attack_protocol():
    st.title("Anxiety Attack Protocol")
    
    # Question 1: Date
    date_selected = st.date_input("Date", value=datetime.date.today())
    
    # Question 2: Time & Severity
    st.subheader("Time & Severity")
    if st.session_state.show_time_severity:
        for i in range(st.session_state.button_count + 1):
            if i < len(st.session_state.times):
                time_selected, severity = st.session_state.times[i]
            else:
                time_selected = datetime.datetime.now(swiss_tz).time()
                severity = 1

            time_selected_str = st.text_input(f"Time {i+1}", value=time_selected.strftime('%H:%M'), key=f"time_input_{i}")
            time_selected = datetime.datetime.strptime(time_selected_str, '%H:%M').time()
            
            severity = st.slider(f"Severity (1-10) {i+1}", min_value=1, max_value=10, value=severity, key=f"severity_slider_{i}")
            
            if len(st.session_state.times) <= i:
                st.session_state.times.append((time_selected, severity))
            else:
                st.session_state.times[i] = (time_selected, severity)

    if st.button("Add Time & Severity"):
        st.session_state.show_time_severity = True
        st.session_state.button_count += 1

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
    
    new_symptom = st.text_input("Add new symptom:")
    if st.button("Add Symptom") and new_symptom:
        st.session_state.symptoms.append(new_symptom)

    for symptom in st.session_state.symptoms:
        st.write(symptom)

    # Question 4: Triggers
    st.subheader("Triggers:")
    triggers = st.multiselect("Select Triggers", ["Stress", "Caffeine", "Lack of Sleep", "Social Event", "Reminder of traumatic event", "Alcohol", "Conflict", "Family problems"])
    
    new_trigger = st.text_input("Add new trigger:")
    if st.button("Add Trigger") and new_trigger:
        st.session_state.triggers.append(new_trigger)

    for trigger in st.session_state.triggers:
        st.write(trigger)

    # Question 5: Did something help against the attack?
    st.subheader("Did something help against the attack?")
    help_response = st.text_area("Write your response here", height=100)
    
    # Save data to CSV
    if st.button("Save Data"):
        time_severity_pairs = [f"{t.strftime('%H:%M')}-{s}" for t, s in st.session_state.times]
        data = [
            st.session_state['username'],
            date_selected,
            ", ".join(time_severity_pairs),
            ", ".join(symptom for symptom in st.session_state.symptoms),
            ", ".join(triggers + st.session_state.triggers),
            help_response
        ]
        save_to_csv(data)
        st.success("Data saved successfully!")

def main():
    init_github()
    init_credentials()

    if not st.session_state['authentication']:
        options = st.sidebar.selectbox("Select a page", ["Login", "Register"])
        if options == "Login":
            login_page()
        elif options == "Register":
            register_page()
    else:
        st.title("FeelNow")
        anxiety_attack_protocol()

        st.header("Saved Entries")
        if st.session_state.github.file_exists(ATTACK_DATA_FILE):
            data = st.session_state.github.read_df(ATTACK_DATA_FILE)
            user_data = data[data['username'] == st.session_state['username']]
            if not user_data.empty:
                st.write("## Anxiety Attack Protocol Data")
                st.table(user_data)
            else:
                st.write("No data available")
        else:
            st.write("No data available")
        
        if st.button("Logout"):
            st.session_state['authentication'] = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
