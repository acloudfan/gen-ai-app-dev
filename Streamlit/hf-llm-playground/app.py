# Exercise : HuggingFace LLM Playground

# Application flow:
# 1. User selects the LLM
# 2. User adjusts the model parameters (optional)
# 3. User provide a query
# 4. Selected model is invoked
# 5. Result is shown to the user

import streamlit as st
from dotenv import load_dotenv
import os

# from langchain_community.llms import HuggingFaceHub
from langchain_community.llms import HuggingFaceEndpoint


# Load the API keys, if running locally
# CHANGE the path to the env file

# If HF space is used then set the env var HUGGINGFACEHUB_API_TOKEN in the settings
try:
    load_dotenv('C:\\Users\\raj\\.jupyter\\.env')
except:
    print("Environment file not found !! MUST find the env var HUGGINGFACEHUB_API_TOKEN to work.")



# Title
st.title('HuggingFace LLM playground')

# Models that can be used
# Add/remove models from this list as needed
models = [
    'mistralai/Mistral-7B-Instruct-v0.2', 
    'google/flan-t5-xxl',
    # 'meta-llama/Meta-Llama-3-8B',
    'tiiuae/falcon-40b-instruct',
]

# Selected model in model_id
model_id = st.sidebar.selectbox(
    'Select model',
    options=tuple(models)
)

# Read the API key from environment - switch key for different providers
# api_token = os.environ.get('HUGGINGFACEHUB_API_TOKEN')

if 'model-response' not in st.session_state:
    st.session_state['model-response'] = '<provide query & click on invoke>'

# draw the box for model response
st.text_area('Response', value = st.session_state['model-response'], height=400)

# draw the box for query
query = st.text_area('Query', placeholder='provide query & invoke', value='who was the president of the USA in 2023?')

# Model parameter controls
# https://api.python.langchain.com/en/latest/llms/langchain_community.llms.huggingface_endpoint.HuggingFaceEndpoint.html

# Temperature
temperature = st.sidebar.slider(
    label='Temperature',
    min_value=0.01,
    max_value=1.0
)

# Top p
top_p = st.sidebar.slider(
    label='Top p',
    min_value=0.01,
    max_value=1.0,
    value=0.01
)

# Top k
top_k = st.sidebar.slider(
    label='Top k',
    min_value=1,
    max_value=50,
    value=10
)

repetition_penalty = st.sidebar.slider(
    label='Repeatition penalty',
    min_value=0.0,
    max_value=5.0,
    value=1.0
)

# Maximum token
max_tokens = st.sidebar.number_input(
    label='Max tokens',
    value=50
)

# Function to create the LLM
def get_llm(model_id):
    return HuggingFaceEndpoint(
        repo_id=model_id, 
        temperature=temperature,
        top_k = top_k,
        top_p = top_p,
        repetition_penalty = repetition_penalty,
        max_new_tokens=max_tokens
    )

# Function for invoking the LLM
def invoke():
    llm_hf = get_llm(model_id)
    
    # Show spinner, while we are waiting for the response
    with st.spinner('Invoking LLM ... '):
        st.session_state['model-response'] = llm_hf.invoke(query)
    

st.button("Invoke", on_click=invoke)