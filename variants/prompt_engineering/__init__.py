import streamlit as st

from utils.input import ui_input

def prompt_engineering():
    st.title("Prompt Engineering Variant")
    
    config = ui_input()
    
    if config:
        st.write(config)