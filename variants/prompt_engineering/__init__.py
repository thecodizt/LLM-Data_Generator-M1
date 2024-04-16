import streamlit as st

from variants.prompt_engineering.input import ui_input
from variants.prompt_engineering.generate import generate

def prompt_engineering():
    st.title("Prompt Engineering Pipeline")
    
    config = ui_input()

    st.write(config)
    
    isStartGenerate = st.button("Generate")
    
    if isStartGenerate:
        response = generate(config)
        
        if response:
            st.write(response)