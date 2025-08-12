# Manages user & assistant messages in the session state.

### 1. Import the libraries
import streamlit as st
import time
import os
from dotenv import load_dotenv
from dataclasses import dataclass

# https://api.python.langchain.com/en/latest/llms/langchain_community.llms.cohere.Cohere.html#langchain_community.llms.cohere.Cohere
from langchain_community.llms import Cohere

### 2. Setup datastructure for holding the messages
# Define a Message class for holding the query/response
@dataclass
class Message:
    role: str       # identifies the actor (system, user or human, assistant or ai)
    payload: str    # instructions, query, response

# Streamlit knows about the common roles as a result, it is able to display the icons
USER = "user"            # or human, 
ASSISTANT = "assistant"  # or ai, 
SYSTEM = "system"

# This is to simplify local development
# Without this you will need to copy/paste the API key with every change
try:
    # CHANGE the location of the file
    load_dotenv('C:\\Users\\raj\\.jupyter\\.env')
    # Add the API key to the session - use it for populating the interface
    if os.getenv('COHERE_API_KEY'):
        st.session_state['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')
except:
    print("Environment file not found !! Copy & paste your Cohere API key.")


### 3. Initialize the datastructure to hold the context
MESSAGES='messages'
if  MESSAGES not in st.session_state:
    system_message  = Message(role=SYSTEM, payload='you are a polite assistant named "Ruby".')
    st.session_state[MESSAGES] = [system_message]

### 4. Setup the title & input text element for the Cohere API key
#    Set the title
#    Populate API key from session if it is available
st.title("Multi-Turn conversation interface  !!!")

# If the key is already available, initialize its value on the UI
if 'COHERE_API_KEY' in st.session_state:
    cohere_api_key = st.sidebar.text_input('Cohere API key',value=st.session_state['COHERE_API_KEY'])
else:
    cohere_api_key = st.sidebar.text_input('Cohere API key',placeholder='copy & paste your API key')




### 5. Define utility functions to invoke the LLM

# Create an instance of the LLM
@st.cache_resource
def  get_llm():
     return Cohere(model="command", cohere_api_key=cohere_api_key) 

# Create the context by concatenating the messages
def get_chat_context():
    context = ''
    for msg in st.session_state[MESSAGES]:
        context = context + '\n\n' + msg.role + ':' + msg.payload
    return context

# Generate the response and return
def  get_llm_response(prompt):
    llm = get_llm()

    # Show spinner, while we are waiting for the response
    with st.spinner('Invoking LLM ... '):
        # get the context
        chat_context = get_chat_context()

        # Prefix the query with context
        query_payload = chat_context +'\n\n Question: ' + prompt

        response = llm.invoke(query_payload)

        return response

### 6. Write the messages to chat_message container
# Write messages to the chat_message element
# This is needed as streamlit re-runs the entire script when user provides input in a widget
# https://docs.streamlit.io/develop/api-reference/chat/st.chat_message
for msg in st.session_state[MESSAGES]:
    st.chat_message(msg.role).write(msg.payload)

### 7. Create the *chat_input* element to get the user query
# Interface for user input
prompt = st.chat_input(placeholder='Your input here')

### 8. Process the query received from user
if prompt:
    # create user message and add to end of messages in the session
    user_message = Message(role=USER, payload=prompt)
    st.session_state[MESSAGES].append(user_message)

    # Write the user prompt as chat message
    st.chat_message(USER).write(prompt)

    # Invoke the LLM
    response = get_llm_response(prompt)

    # Create message object representing the response
    assistant_message = Message(role=ASSISTANT, payload=response)

    # Add the response message to the mesages array in the session
    st.session_state[MESSAGES].append(assistant_message)

    # Write the response as chat_message
    st.chat_message(ASSISTANT).write(response)

### 9. Write out the current content of the context
st.divider()
st.subheader('st.session_state[MESSAGES] dump:')

# Print the state of the buffer
for msg in st.session_state[MESSAGES]:
    st.text(msg.role + ' : ' + msg.payload)
