import streamlit as st
from PIL import Image
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main_attack():
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["main"])[0]

      if page == "anxiety_attack_protocol":
        attack_protocol.show()
    elif page == "anxiety_protocol":
        anxiety_protocol.show()     
    else:
        show()

def show():
    st.image("Logo.jpeg", width=600)
    st.write("---")

    st.write("Anxiety Assessment:")

    answer = st.radio("Do you feel like you're having an Anxiety Attack right now?", ("Yes", "No"))
    if answer == "Yes":
        st.switch_pages("pages/anxiety_attack_protocol.py")
    else:
        answer_2 = st.radio("Are you anxious right now?", ("Yes", "No"))
        if answer_2 == "Yes":
            st.switch_pages("pages/anxiety_protocol.py")
        else:
            st.write("Reassess your feelings.")

def switch_pages(page_name):
    st.success("Redirecting to {} page...".format(page_name))
    time.sleep(3)
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

if __name__ == "__main__":
    main_attack() 
