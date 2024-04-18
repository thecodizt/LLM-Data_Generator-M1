import streamlit as st
import ollama
import pandas as pd

from variants.prompt_engineering.utils import generate_record_schema, extract_yaml_snippets, find_matching_snippet

def generate(config):
    target_count = config["num_records"]
    primary_keys = [config["column_info"][i]["col_name"] for i in range(config["num_columns"]) if config["column_info"][i]["is_primary"]]
    all_generations = pd.DataFrame()
    valid_generations = pd.DataFrame()
    columns = [config["column_info"][i]["col_name"] for i in range(config["num_columns"])]
    schema = generate_record_schema(columns)
    
    total_iterations = 0
    
    prompt = create_message(config)
    if prompt:
        prompt_expander = st.expander("Prompt given to the LLM")
        prompt_expander.write(prompt)
        
    st.subheader("Latest Reponse")
    latest_response = st.empty()

    # Define Streamlit components outside the loop
    col1, col2, col3, col4 = st.columns(4)
    total_iterations_metric = col1.empty()
    all_generations_metric = col2.empty()
    valid_generations_metric = col3.empty()
    hit_rate_metric = col4.empty()

    

    while len(valid_generations) < target_count and len(all_generations) <= 10*len(valid_generations):
        
        total_iterations += 1
        
        response = ollama.generate(model=config["llm_model"], prompt=prompt)["response"]
        if response:
            latest_response.write(response)
        yaml_snippets = extract_yaml_snippets(response)
        match = find_matching_snippet(schema=schema, snippets=yaml_snippets)
        if match is not None and isinstance(match, dict):
            # Convert the match to a DataFrame and add to all_generations
            match_df = pd.DataFrame([match], columns=columns)
            
            all_generations = pd.concat([all_generations, match_df], ignore_index=True)

            # Remove duplicates from all_generations to create valid_generations
            if len(primary_keys)>0:
                valid_generations = all_generations.drop_duplicates(subset=primary_keys)
            else:
                valid_generations = all_generations
            
        # Update Streamlit components inside the loop
        total_iterations_metric.metric("Total Iterations", total_iterations)
        all_generations_metric.metric("All Generations", len(all_generations))
        valid_generations_metric.metric("Valid Generations", len(valid_generations))
        hit_rate_metric.metric("Failure Rate", 1-(len(valid_generations)/total_iterations))

    if len(primary_keys) > 0:
        return all_generations.drop_duplicates(subset=primary_keys)
    else:
        return all_generations

def create_message(config):
    
    prompt = f'''
    BASE:
    Generate an entity based on the given context with the specified properties in YAML format. Use the optional sample data provided as well. Provide only one instance of the record and it's never nested. Give only one set of values in the schema. Do not add any additional fields.
    
    CONTEXT:
    {config["base_context"]}
    
    Expected properties:
    '''
    
    for i in range(config["num_columns"]):
        prompt += f'''
        {config["column_info"][i]["col_name"]}: {config["column_info"][i]["col_desc"]}
        '''
    
    prompt += '''
     
     Follow the following YAML Schema:
     
     ```yaml
     RECORD:
     '''
     
    for i in range(config["num_columns"]):
        prompt += f'''
        {config["column_info"][i]["col_name"]}: [generated value]
        '''
        
    prompt += '''
    ```
    
    GENERATED VALUES:
    '''
    
    return prompt