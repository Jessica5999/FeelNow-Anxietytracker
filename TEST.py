import streamlit as st
import datetime

github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"])


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
    symptoms_anxiety = st.checkbox("Anxiety")
    symptoms_palpitations = st.checkbox("Palpitations")
    symptoms_sweating = st.checkbox("Sweating")
    symptoms_trembling = st.checkbox("Trembling")
    symptoms_nausea = st.checkbox("Nausea")
    symptoms_dizziness = st.checkbox("Dizziness")
    symptoms_cold = st.checkbox("Cold Hands")
    symptoms_cold2 = st.checkbox("Cold")
    symptoms_nervous = st.checkbox("Nervousness")
    symptoms_tremor = st.checkbox("Tremor")
    symptoms_shortbreath = st.checkbox("Shortness of Breath")

    # Question 4: Triggers
    st.subheader("Triggers:")
    triggers = st.multiselect("Select Triggers", ["Stress", "Caffeine", "Lack of Sleep", "Other"])

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
        
        time_selected = st.time_input(f"Time {i+1}", value=time_selected)
        severity = st.slider(f"Severity (1-10) {i+1}", min_value=1, max_value=10, value=severity)
        
        # Update time and severity in session state
        st.session_state.times[i] = (time_selected, severity)

    if st.button("Add Time & Severity"):
        st.session_state.button_count += 1


def main_page():
    st.title("FeelNow")
    anxiety_attack_protocol()

if __name__ == "__main__":
    main_page()
