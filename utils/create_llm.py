from langchain.llms import Cohere

# pip install -U langchain-cohere
# from langchain_cohere import Cohere


from langchain_openai import OpenAI


from langchain_community.llms.ai21 import AI21
from langchain_anthropic import AnthropicLLM
from langchain_community.llms import HuggingFaceEndpoint
from langchain_openai import ChatOpenAI

# Cohere
## Create the Cohere model
def create_cohere_llm(args={}):
    llm = Cohere(**args) 
    return llm


# OpenAI
## Create the OpenAI model
def create_gpt_llm(args={}):
    llm = ChatOpenAI(**args) 
    return llm



# AI21
## Create the AI21 Jurassic model
def create_ai21_llm(args={}):
    llm = AI21(**args)
    
    return llm

# Anthropic
## Create the Anthropic Claude models
def create_anthropic_llm(args={}):
    llm = AnthropicLLM(**args)

    return llm

# HuggingFace
## Create a hugging face model
## Default model = 
def create_hugging_face_llm(repo_id="mistralai/Mistral-7B-Instruct-v0.2", args={}):
    
    llm = HuggingFaceEndpoint(
        repo_id = repo_id,
        **args
    )
    
    return llm