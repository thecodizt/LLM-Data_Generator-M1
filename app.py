import streamlit as st

from variants.prompt_engineering import prompt_engineering

def main():
    main_choice = None
    with st.sidebar:
        st.header("LLM Based Data Generation")
        
        main_choice = st.radio(
            label = "",
            options = [ "**Baseline Evaluation**", "**Causal Language Modeling**", "**Masked Language Modeling**"], 
            captions = ["Engineer the prompts passed to LLM", "Use summarization like results and parse", "Use Masks to indicate areas to generate data"], 
            index=0 # set to choice during devalopment
        )
    
    if main_choice == "**Baseline Evaluation**":
        prompt_engineering()
    elif main_choice == "**Causal Language Modeling**":
        st.title("Causal Language Modeling")
        st.write("In Progress")
    elif main_choice == "**Masked Language Modeling**":
        st.title("Masked Language Modeling")
        st.write("In Progress")
    else:
        st.error("Select an option from sidebar")

if __name__ == "__main__":
    main()