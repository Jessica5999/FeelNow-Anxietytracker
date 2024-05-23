import streamlit as st
from PIL import Image
import time
import sys
import os

def show_main_page():
    st.image("Logo.jpeg", width=600)
    st.write("---")

    st.write("Anxiety Assessment:")

    answer = st.radio("Are you anxious right now, without having an attack?", ("Yes", "No"))
    if answer == "Yes":
        st.switch_page("pages/anxiety_protocol.py")
    else:
        answer_2 = st.radio("Do you feel like you're having an Anxiety Attack right now?", ("Yes", "No"))
        if answer_2 == "Yes":
            st.switch_page("pages/attack_protocol.py")
        else:
            st.write("Reassess your feelings")

def switch_page(page_name):
    st.success(f"Redirecting to {page_name.replace('_', ' ')} page...")
    time.sleep(3)
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

if __name__ == "__main__":
    show_main_page()
