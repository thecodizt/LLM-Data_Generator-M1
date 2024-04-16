import ollama

def generate(config):
    
    prompt = create_message(config)
    
    response = ollama.chat(model="mistral", messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    
    return response["message"]["content"]

def create_message(config):
    
    prompt = f'''
    BASE:
    Generate an entity based on the given context with the specified properties in YAML format. Use the optional sample data provided as well
    
    CONTEXT:
    {config["base_context"]}
    
    PROPERTIES:
    '''
    
    for i in range(config["num_columns"]):
        prompt += f'''
        {config["column_info"][i]["col_name"]}: {config["column_info"][i]["col_desc"]}
        '''
    
    print(prompt)
    
    return prompt