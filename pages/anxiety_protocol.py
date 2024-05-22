import streamlit as st
import pandas as pd
import datetime

# Konstanten
DATA_FILE = "anxiety_data.csv"

def show():
    st.title("Anxiety Protocol")

def anxiety_protocol():
    if 'data' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE):
            st.session_state.data = st.session_state.github.read_df(DATA_FILE)
        else:
            st.session_state.data = pd.DataFrame(columns=['Date', 'Location', 'Anxiety Description', 'Cause', 'Triggers', 'Symptoms', 'Help Response'])

    st.write("Anxiety Protocol Page")

    # Question 1: Date
    date_selected = st.date_input("Date", value=datetime.date.today())

    # Question 2: Where are you and what is the environment?
    location = st.text_area("Where are you and what is the environment?", key="location", height=100)

    anxiety_description = st.text_area("Try to describe your anxiety right now?", key="anxiety_description", height=100)

    cause = st.text_area("What do you think could be the cause?", key="cause", height=100)
    
    triggers = st.text_area("Any specific triggers? For example Stress, Caffeine, Lack of Sleep, Social Event, Reminder of traumatic event", key="triggers", height=100)

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
    
    symptoms_list = [symptoms_chestpain, symptoms_chills, symptoms_cold, symptoms_coldhands, symptoms_dizziness, symptoms_feelingdanger, 
                     symptoms_heartracing, symptoms_hotflushes, symptoms_nausea, symptoms_nervous, symptoms_numbhands, symptoms_numbness, 
                     symptoms_shortbreath, symptoms_sweating, symptoms_tensemuscles, symptoms_tinglyhands, symptoms_trembling, symptoms_tremor, 
                     symptoms_weakness]
    
    symptoms = [symptom for i, symptom in enumerate(["Chest Pain", "Chills", "Cold", "Cold Hands", "Dizziness", "Feeling of danger", 
                                                      "Heart racing", "Hot flushes", "Nausea", "Nervousness", "Numb Hands", "Numbness", 
                                                      "Shortness of Breath", "Sweating", "Tense Muscles", "Tingly Hands", "Trembling", 
                                                      "Tremor", "Weakness"]) if symptoms_list[i]]
    
    symptoms_text = ', '.join(symptoms)

    # Question 5: Did something Help against the attack?
    help_response = st.text_area("Did something Help against the Anxiety?", key="help_response", height=100)

    if st.button("Save Entry"):
        new_entry = {
            'Date': date_selected,
            'Location': location,
            'Anxiety Description': anxiety_description,
            'Cause': cause,
            'Triggers': triggers,
            'Symptoms': symptoms_text,
            'Help Response': help_response
        }
        st.session_state.data = st.session_state.data.append(new_entry, ignore_index=True)
        st.session_state.github.write_df(DATA_FILE, st.session_state.data, "added new entry")
        st.success("Entry saved successfully!")

    # Display saved entries
    st.subheader("Saved Entries")
    st.write(st.session_state.data)

def main_page():
    st.title("FeelNow")
    anxiety_protocol()

if __name__ == "__main__":
    main_page()

