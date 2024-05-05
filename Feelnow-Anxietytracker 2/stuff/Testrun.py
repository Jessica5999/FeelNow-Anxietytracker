from github_contents import GithubContents
import streamlit as st

st.set_page_config(page_title="feelnow")

github = GithubContents(
    st.secrets["github"]["owner"]
    st.secrets["github"]["repo"]
    st.secrets["github"]["token"])

