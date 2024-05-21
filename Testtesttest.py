pip install streamlit pandas
import streamlit as st
import pandas as pd
from pages import Mainpage, Login, Attack, Anxiety_Attack_Protocol, Anxiety_protocol
from github_contents import GithubContents

# Initialize GithubContents
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"]
)

# Page title map
PAGE_TITLE_MAP = {
    "Main Page": Mainpage,
    "Login Page": Login,
    "Register Page": Attack,
    "Anxiety Attack Protocol Page": Anxiety_Attack_Protocol,
    "Anxiety Protocol Page": Anxiety_protocol
}

# Function to save input data to a CSV file
def save_input_to_csv(data, filename="user_data.csv"):
    try:
        # Read existing data
        existing_data = pd.read_csv(filename)
        data_df = pd.DataFrame([data])
        updated_data = pd.concat([existing_data, data_df], ignore_index=True)
    except FileNotFoundError:
        # File does not exist, create a new one
        updated_data = pd.DataFrame([data])
    
    updated_data.to_csv(filename, index=False)
    st.success(f"Data saved to {filename}")

# Streamlit App Logic
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGE_TITLE_MAP.keys()))

# Display selected page
Page = PAGE_TITLE_MAP[selection]
Page.display()

# Sample input form to demonstrate saving inputs
st.sidebar.title("Anxiety_protocol")
if st.sidebar.button("Submit Input"):
    user_input = {
        "symptoms_cold": st.checkbox("Cold"),
    }
    save_input_to_csv(user_input)



