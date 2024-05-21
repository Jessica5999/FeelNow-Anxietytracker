import streamlit as st
import pandas as pd
import datetime
from github_contents import GithubContents

# GitHub-Verbindungsinformationen
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"]
)

# Laden der CSV-Datei oder Initialisieren, wenn sie nicht existiert
csv_file = "data.csv"
try:
    data = pd.read_csv(csv_file)
except FileNotFoundError:
    data = pd.DataFrame(columns=["Page", "Date", "Username", "Password", "Location", "Anxiety Description", "Cause", "Triggers", "Symptoms", "Help Response"])
def save_to_csv(new_data):
    global data
    data = pd.concat([data, pd.DataFrame([new_data])], ignore_index=True)
    data.to_csv(csv_file, index=False)
    github.upload_file(csv_file)
def save_to_csv(new_data):
    global data
    data = pd.concat([data, pd.DataFrame([new_data])], ignore_index=True)
    data.to_csv(csv_file, index=False)
    github.upload_file(csv_file)
def save_login_data(username, password):
    new_data = {
        "Page": "Login Page",
        "Date": datetime.datetime.now().isoformat(),
        "Username": username,
        "Password": password,
        "Location": None,
        "Anxiety Description": None,
        "Cause": None,
        "Triggers": None,
        "Symptoms": None,
        "Help Response": None
    }
    save_to_csv(new_data)
def save_anxiety_data(date_selected, username, location_description, anxiety_description, cause_description, triggers_description, selected_symptoms, help_response):
    new_data = {
        "Page": "Anxiety Attack Protocol Page",
        "Date": date_selected.isoformat(),
        "Username": username,
        "Password": None,
        "Location": location_description,
        "Anxiety Description": anxiety_description,
        "Cause": cause_description,
        "Triggers": triggers_description,
        "Symptoms": ', '.join(selected_symptoms),
        "Help Response": help_response
    }
    save_to_csv(new_data)
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

        # Frage 6: Symptome
        st.subheader("Symptoms:")
        col1, col2 = st.columns(2)
        selected_symptoms = []
        with col1:
            if st.checkbox("Chest Pain"):
                selected_symptoms.append("Chest Pain")
            if st.checkbox("Chills"):
                selected_symptoms.append("Chills")
            if st.checkbox("Cold"):
                selected_symptoms.append("Cold")
            if st.checkbox("Cold Hands"):
                selected_symptoms.append("Cold Hands")
            if st.checkbox("Dizziness"):
                selected_symptoms.append("Dizziness")
            if st.checkbox("Feeling of danger"):
                selected_symptoms.append("Feeling of danger")
            if st.checkbox("Heart racing"):
                selected_symptoms.append("Heart racing")
            if st.checkbox("Hot flushes"):
                selected_symptoms.append("Hot flushes")
        with col2:
            if st.checkbox("Nausea"):
                selected_symptoms.append("Nausea")
            if st.checkbox("Nervousness"):
                selected_symptoms.append("Nervousness")
            if st.checkbox("Numb Hands"):
                selected_symptoms.append("Numb Hands")
            if st.checkbox("Numbness"):
                selected_symptoms.append("Numbness")
            if st.checkbox("Shortness of Breath"):
                selected_symptoms.append("Shortness of Breath")
            if st.checkbox("Sweating"):
                selected_symptoms.append("Sweating")
            if st.checkbox("Tense Muscles"):
                selected_symptoms.append("Tense Muscles")
            if st.checkbox("Tingly Hands"):
                selected_symptoms.append("Tingly Hands")
            if st.checkbox("Trembling"):
                selected_symptoms.append("Trembling")
            if st.checkbox("Tremor"):
                selected_symptoms.append("Tremor")
            if st.checkbox("Weakness"):
                selected_symptoms.append("Weakness")

        # Frage 7: Did something Help against the anxiety?
        st.subheader("Did something Help against the Anxiety?")
        help_response = st.text_area("Write your response here", key="help_response", height=100)

        if st.button("Submit"):
            username = st.text_input("Username for Record")  # Assuming you have a way to link this with the user
            save_anxiety_data(date_selected, username, location_description, anxiety_description, cause_description, triggers_description, selected_symptoms, help_response)
            st.success("Data saved successfully!")

if __name__ == "__main__":
    main()

