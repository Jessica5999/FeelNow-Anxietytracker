import streamlit as st
import pandas as pd
from datetime import date
from github_contents import GithubContents

# Set constants
DATA_FILE = "Account_data.csv"
DATA_COLUMNS = ["Name", "Nachname", "Geburtsdatum"]

# Set page configuration
st.set_page_config(page_title="Feelnow", page_icon="🧠", layout="wide",  
                   initial_sidebar_state="expanded")

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])

def init_dataframe():
    """Initialize or load the dataframe."""
    if 'df' in st.session_state:
        pass
    elif st.session_state.github.file_exists(DATA_FILE):
        st.session_state.df = st.session_state.github.read_df(DATA_FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)
