from langchain_cohere import ChatCohere
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


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

