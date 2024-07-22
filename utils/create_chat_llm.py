from langchain_cohere import ChatCohere
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
# from langchain_community.llms import HuggingFaceEndpoint, ChatHuggingFace

# !pip install -U langchain-huggingface
# https://api.python.langchain.com/en/latest/chat_models/langchain_huggingface.chat_models.huggingface.ChatHuggingFace.html
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint


def create_cohere_chat_llm(args={}):
    llm = ChatCohere(**args) 
    return llm

# 
def create_gpt_chat_llm(args={}):
    llm = ChatOpenAI(**args) 
    return llm

## Create the Anthropic Claude models
def create_anthropic_chat_llm(args={}):
    llm = ChatAnthropic(**args)

    return llm

## Create ChatOpenAI
def create_gpt_chat_llm(args={}):
    llm = ChatOpenAI(**args) 
    return llm

# HuggingFace
## Create a hugging face model
## Default model = 
def create_hugging_face_chat_llm(repo_id="mistralai/Mistral-7B-Instruct-v0.2", args={}, verbose=False):
    
    llm = HuggingFaceEndpoint(
        repo_id = repo_id,
        **args
    )

    chat_llm = ChatHuggingFace(llm=llm, verbose=verbose)
    
    return chat_llm