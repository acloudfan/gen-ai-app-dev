# This is to demonstrate the core logic for the project

# 1. Get the link to PDF
# 2. Read the content of the PDF
# 3. Iterate:
#    3.1 Create a chunk (set of pages)
#    3.2 Create summary by combining partial summary & chunk


### 1. Import the libraries
import streamlit as st
import time
import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate

# from langchain_community.llms import HuggingFaceHub
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.document_loaders import PyPDFLoader

# This is to simplify local development
# Without this you will need to copy/paste the API key with every change
try:
    # CHANGE the location of the file
    load_dotenv('C:\\Users\\raj\\.jupyter\\.env1')
    # Add the API key to the session - use it for populating the interface
    if os.getenv('HUGGINGFACEHUB_API_TOKEN'):
        st.session_state['HUGGINGFACEHUB_API_TOKEN'] = os.getenv('HUGGINGFACEHUB_API_TOKEN')
    else:
        st.session_state['HUGGINGFACEHUB_API_TOKEN'] = ''
except:
    print("Environment file not found !! Copy & paste your HuggingFace API key.")


# Prompt to be used
template = """
    extend the abstractive summary below with the new content. Keep total size of the extended summary around 3000 words.

    summary: 
    {summary}

    new content:
    {content}

    extended summary:
    
"""

prompt_template = PromptTemplate(
    input_variables = ['summary', 'content'],
    template = template
)

# Model for summarization
model_id = 'mistralai/Mistral-7B-Instruct-v0.2'
CONTEXT_WINDOW_SIZE=32000
MAX_TOKENS=2000


if 'SUMMARY' not in st.session_state:
    st.session_state['SUMMARY'] = ''

if 'HUGGINGFACEHUB_API_TOKEN' not in st.session_state:
    st.session_state['HUGGINGFACEHUB_API_TOKEN'] = ''


# function to generate the summary
def generate_summary():
    
    # Create an LLM
    llm = HuggingFaceEndpoint(
        repo_id=model_id, 
        max_new_tokens=MAX_TOKENS,
        huggingfacehub_api_token = hugging_face_api_key
    )

    # Show spinner, while we are waiting for the response
    with st.spinner('Invoking LLM ... '):
        # 1. Load the PDF file
        partial_summary = ''
        loader = PyPDFLoader(pdf_link)
        pages = loader.load()
        page_count = len(pages)
        print("Number of pages = ", page_count)

        # 2. Iterate to generate the summary
        
        next_page_index = 0
        while next_page_index < len(pages):
            'Processing chunk, starting with page index : ',next_page_index

            # Holds the chunk = a set of contenated pages
            new_content = ''
            
            # Loop to create chunk 
            for i, doc in enumerate(pages[next_page_index : ]):
                last_i = i
                if len(partial_summary) + len(new_content) + len(doc.page_content) + MAX_TOKENS < CONTEXT_WINDOW_SIZE :
                    new_content = new_content + doc.page_content
                else:
                    break
                    
            # Initialize the new content and next page index
            next_page_index = next_page_index + last_i + 1
                
            # Pass the current summary and new content to LLM for summarization
            query = prompt_template.format(summary=partial_summary, content=new_content)
            
            

            partial_summary = llm.invoke(query)
        st.session_state['SUMMARY'] = partial_summary
        

# Title
st.title('PDF Summarizer')

if 'HUGGINGFACEHUB_API_TOKEN' in st.session_state:
    hugging_face_api_key = st.sidebar.text_input('HuggingFace API key',value=st.session_state['HUGGINGFACEHUB_API_TOKEN'])
else:
    hugging_face_api_key = st.sidebar.text_input('HuggingFace API key',placeholder='copy & paste your API key')


# draw the box for query
pdf_link = st.text_input('Link to PDF document', placeholder='copy/paste link to the PDF', value='https://sgp.fas.org/crs/misc/R47644.pdf')

# button
st.button("Generate sumary", on_click=generate_summary)


st.text_area('Response', value = st.session_state['SUMMARY'], height=800)
 