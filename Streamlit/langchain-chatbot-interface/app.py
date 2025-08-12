# Manages user & assistant messages in the session state.

### 1. Import the libraries
import streamlit as st
import time
import os
from dotenv import load_dotenv

from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

# This is to simplify local development
# Without this you will need to copy/paste the API key with every change
try:
    # CHANGE the location of the file
    load_dotenv('C:\\Users\\raj\\.jupyter\\.env1')
    # Add the API key to the session - use it for populating the interface
    if os.getenv('OPENAI_API_KEY'):
        st.session_state['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
except:
    print("Environment file not found !! Copy & paste your OpenAI API key.")


### 1. Setup the title & input text element for the OpenAI API key
#    Set the title
#    Populate API key from session if it is available
st.title("LangChain ConversationSummaryMemory  !!!")

# If the key is already available, initialize its value on the UI
if 'OPENAI_API_KEY' in st.session_state:
    openai_api_key = st.sidebar.text_input('OpenAI API key',value=st.session_state['OPENAI_API_KEY'])
else:
    openai_api_key = st.sidebar.text_input('OpenAI API key',placeholder='copy & paste your OpenAI API key')

if len(openai_api_key) == 0 :
    "provide valid OpenAI API Key !!"
    st.stop()

# print(type(openai_api_key))
# st.stop()
### 2. Define utility functions to invoke the LLM

# Create an instance of the LLM for summarization
@st.cache_resource
def  get_summarization_llm():
     model = 'gpt-3.5-turbo-0125'
     return ChatOpenAI(model=model, openai_api_key=openai_api_key) 

# Create an instance of the LLM for chatbot responses
@st.cache_resource
def  get_llm():
     model = 'gpt-3.5-turbo-0125'
     return ChatOpenAI(model=model, openai_api_key=openai_api_key) 

@st.cache_resource
def get_llm_chain():
    memory = st.session_state['MEMORY']
    conversation = ConversationChain(
        llm=get_llm(),
        # prompt=prompt_template,
        # verbose=True,
        memory=memory
    )
    return conversation

# Create the context by concatenating the messages
def get_chat_context():
    memory = st.session_state['MEMORY']
    return memory.buffer

# Generate the response and return
def  get_llm_response(prompt):
    # llm = get_llm()
    llm = get_llm_chain()

    # Show spinner, while we are waiting for the response
    with st.spinner('Invoking LLM ... '):
        # get the context
        chat_context = get_chat_context()

        # Prefix the query with context
        query_payload = chat_context +'\n\n Question: ' + prompt

        response = llm.invoke(query_payload)

        return response

# Initialize the session state memory
if 'MEMORY' not in st.session_state :
    memory = ConversationSummaryMemory(
        llm = get_summarization_llm(),
        human_prefix='user',
        ai_prefix = 'assistant',
        return_messages=True
    )
    # add to the session
    st.session_state['MEMORY'] = memory

### 3. Write the messages to chat_message container
# Write messages to the chat_message element
# This is needed as streamlit re-runs the entire script when user provides input in a widget
# https://docs.streamlit.io/develop/api-reference/chat/st.chat_message


# Check to ensure that a valid key is provided
if  len(openai_api_key) > 0:
    for msg in st.session_state['MEMORY'].chat_memory.messages:

        if (isinstance(msg, HumanMessage)):
            st.chat_message('user').write(msg.content)
        elif (isinstance(msg, AIMessage)):
            st.chat_message('ai').write(msg.content)
        else:
            print('System message: ', msg.content)
        

    ### 4. Create the *chat_input* element to get the user query
    # Interface for user input
    prompt = st.chat_input(placeholder='Your input here')

    ### 5. Process the query received from user
    if prompt and openai_api_key:

        # Write the user prompt as chat message
        st.chat_message('user').write(prompt)

        # Invoke the LLM
        response = get_llm_response(prompt)

        # Write the response as chat_message
        st.chat_message('ai').write(response['response'])

    ### 6. Write out the current content of the context
    st.divider()
    st.subheader('Context/Summary:')

    # Print the state of the buffer
    st.session_state['MEMORY'].buffer
