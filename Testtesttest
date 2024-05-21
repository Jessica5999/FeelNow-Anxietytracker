import streamlit as st
import pandas as pd
from github_contents import GithubContents

# GitHub-Verbindungsinformationen
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"]
)

# Laden der CSV-Datei
csv_file = "data.csv"
data = pd.read_csv(csv_file)

# Funktionen zum Speichern von Daten in der CSV-Datei
def save_login_data(username, password):
    new_row = pd.DataFrame({"Username": [username], "Password": [password]})
    data = pd.concat([data, new_row], ignore_index=True)
    data.to_csv(csv_file, index=False)
    github.upload_file(csv_file)

# Hier fügen Sie die Funktionen für die anderen Seiten hinzu, um die entsprechenden Daten zu speichern

# Beispiel-Streamlit-App
def main():
    st.title("Data Entry App")

    # Seiten-Navigation
    page_selection = st.radio("Go to page:", ("Login Page", "Anxiety Attack Protocol Page", "Anxiety Protocol Page"))

    if page_selection == "Login Page":
        st.subheader("Login Page")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            save_login_data(username, password)
            st.success("Login successful!")
    elif page_selection == "Anxiety Attack Protocol Page":
        st.subheader("Anxiety Attack Protocol Page")
        # Hier fügen Sie die Eingabefelder für die Anxiety Attack Protocol Page hinzu

    # Frage 1: Datum
    date_selected = st.date_input("Date", value=datetime.date.today())

    # Frage 2: Zeit & Schweregrad
    st.subheader("Time & Severity")
    add_time_severity()

    # Frage 3: Symptome
    st.subheader("Symptoms:")
    col1, col2 = st.columns(2)
    with col1:
        symptoms_anxiety = st.checkbox("Anxiety")
        symptoms_chestpain = st.checkbox("Chest Pain")
        symptoms_chills = st.checkbox("Chills")
        symptoms_chocking = st.checkbox("Choking")
        symptoms_cold = st.checkbox("Cold")
        symptoms_coldhands = st.checkbox("Cold Hands")
        symptoms_dizziness = st.checkbox("Dizziness")
        symptoms_feelingdanger = st.checkbox("Feeling of Danger")
        symptoms_feelingdread = st.checkbox("Feeling of Dread")
        symptoms_heartracing = st.checkbox("Heart Racing")
        symptoms_hotflushes = st.checkbox("Hot Flushes")
        symptoms_irrationalthinking = st.checkbox("Irrational Thinking")
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

    # Frage 4: Auslöser
    st.subheader("Triggers:")
    triggers = st.multiselect("Select Triggers", ["Stress", "Caffeine", "Lack of Sleep", "Social Event", "Reminder of traumatic event", "Alcohol", "Conflict", "Family problems"])

    # Frage 5: Hat etwas gegen den Anfall geholfen?
    st.subheader("Did something Help against the attack?")
    help_response = st.text_area("Write your response here", height=100)

    # Speichern der Daten beim Klicken des "Submit"-Buttons
    if st.button("Submit"):
        save_anxiety_data(date_selected, symptoms_anxiety, symptoms_chestpain, symptoms_chills, symptoms_chocking, symptoms_cold, symptoms_coldhands, symptoms_dizziness, symptoms_feelingdanger, symptoms_feelingdread, symptoms_heartracing, symptoms_hotflushes, symptoms_irrationalthinking, symptoms_nausea, symptoms_nervous, symptoms_numbhands, symptoms_numbness, symptoms_palpitations, symptoms_shortbreath, symptoms_sweating, symptoms_tensemuscles, symptoms_tinglyhands, symptoms_trembling, symptoms_tremor, symptoms_weakness, triggers, help_response)
        st.success("Data saved successfully!")

    elif page_selection == "Anxiety Protocol Page":
        st.subheader("Anxiety Protocol Page")
        # Hier fügen Sie die Eingabefelder für die Anxiety Protocol Page hinzu

if __name__ == "__main__":
    main()
elif page_selection == "Anxiety Protocol Page":
    st.subheader("Anxiety Protocol Page")

    # Frage 1: Datum
    date_selected = st.date_input("Date", value=datetime.date.today())

    # Frage 2: Where are you and what is the environment?
    st.subheader("Where are you and what is the environment?")
    location_description = st.text_area("Write your response here", key="location", height=100)

    # Frage 3: Try to describe your anxiety right now
    st.subheader("Try to describe your anxiety right now?")
    anxiety_description = st.text_area("Write your response here", key="anxiety_description", height=100)

    # Frage 4: What do you think could be the cause?
    st.subheader("What do you think could be the cause?")
    cause_description = st.text_area("Write your response here", key="cause", height=100)

    # Frage 5: Any specific triggers?
    st.subheader("Any specific triggers? For example Stress, Caffeine, Lack of Sleep, Social Event, Reminder of traumatic event")
    triggers_description = st.text_area("Write your response here", key="triggers", height=100)

    # Frage 6: Symptoms
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

    # Frage 7: Did something Help against the anxiety?
    st.subheader("Did something Help against the Anxiety?")
    help_response = st.text_area("Write your response here", key="help_response", height=100)
