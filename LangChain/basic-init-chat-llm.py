# Import required libraries
from langchain.chat_models import init_chat_model 
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

# 1. Load API keys from .env file
from dotenv import load_dotenv
load_dotenv('C:\\Users\\raj\\.jupyter\\.env')  # Path to your API keys

# 2. Create chat template with instructions
template = ChatPromptTemplate.from_messages(
    [
        # Set AI's personality
        SystemMessage(content="You are a sarcastic comedian"),
        # User's question with {topic} placeholder
        ("human","Tell me a joke about {topic}")
    ]
)

# 3. Initialize the chat model (GPT-4 mini from OpenAI)
chat_llm = init_chat_model(model="gpt-4o-mini", model_provider="openai")

# 4. Use the model to get a joke about cats
messages = template.format(topic="cat")  # Insert "cat" as the topic
response = chat_llm.invoke(messages)     # Get AI response

# Print the joke
print(response.content)