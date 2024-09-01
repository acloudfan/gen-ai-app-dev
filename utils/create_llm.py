from langchain.llms import Cohere

# pip install -U langchain-cohere
# from langchain_cohere import Cohere


import os
import sys


from langchain_openai import OpenAI


from langchain_community.llms.ai21 import AI21
from langchain_anthropic import AnthropicLLM
# from langchain_community.llms import HuggingFaceEndpoint
from langchain_huggingface import HuggingFaceEndpoint
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI

from utils.api_key_check_utility import api_key_check

# Cohere
## Create the Cohere model
# Model name passed in args
# https://python.langchain.com/v0.2/docs/integrations/providers/cohere/
# https://python.langchain.com/v0.2/api_reference/cohere/llms/langchain_cohere.llms.Cohere.html
# Models : https://docs.cohere.com/docs/models
def create_cohere_llm(args={}, api_key_prompt=False):

    # Check availability in eviroment variable, if not found prompt 
    if api_key_prompt:
        api_key = api_key_check("COHERE_API_KEY")
    
    llm = Cohere(**args) 
    return llm


# OpenAI
## Create the OpenAI model
def create_gpt_llm(args={}, api_key_prompt=False):

    # Check availability in eviroment variable, if not found prompt 
    if api_key_prompt:
        api_key = api_key_check("OPENAI_API_KEY")

    
    llm = OpenAI(**args) 
    return llm



# AI21
## Create the AI21 Jurassic model
def create_ai21_llm(args={}, api_key_prompt=False):

    if api_key_prompt:
        api_key = api_key_check("AI21_API_KEY")
        
    
    llm = AI21(**args)
    
    return llm

# Anthropic
## Create the Anthropic Claude models
def create_anthropic_llm(args={}, api_key_prompt=False):

    # Check availability in eviroment variable, if not found prompt 
    if api_key_prompt:
        api_key = api_key_check("ANTHROPIC_API_KEY")
    
    llm = AnthropicLLM(**args)

    return llm

# HuggingFace
## Create a hugging face model
## https://python.langchain.com/v0.2/api_reference/huggingface/llms/langchain_huggingface.llms.huggingface_endpoint.HuggingFaceEndpoint.html
## Default model = 
def create_hugging_face_llm(repo_id="mistralai/Mistral-7B-Instruct-v0.2", args={}, api_key_prompt=False):
    
    # Check availability in eviroment variable, if not found prompt 
    if api_key_prompt:
        api_key = api_key_check("HUGGINGFACEHUB_API_TOKEN")

    # check if args has model key
    if "model" not in args:
        print('adding.............')
        print(args)
        args['model'] = repo_id
        
    llm = HuggingFaceEndpoint(
        repo_id = repo_id,
        **args
    )
    
    return llm

# Google AI API
# https://api.python.langchain.com/en/latest/llms/langchain_google_genai.llms.GoogleGenerativeAI.html
# pip install --upgrade --quiet  langchain-google-genai
def create_google_llm(model='gemini-1.5-flash', args={}, api_key_prompt=False):

    # Check availability in eviroment variable, if not found prompt 
    if api_key_prompt:
        api_key = api_key_check("GOOGLE_API_KEY")
    
    GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
    llm = GoogleGenerativeAI(model=model,google_api_key=GOOGLE_API_KEY, **args)

    return llm