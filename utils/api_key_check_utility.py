# Utility that checks for the availability of the API key in the environment variable
# If the key is not found in the environment, user is prompted to provide it.
# The receieved key is the added to the environment

import os
import getpass

class api_key_check:
    
    key_names_for_reference = [
        "GOOGLE_API_KEY", "HUGGINGFACEHUB_API_TOKEN", "OPENAI_API_KEY", "COHERE_API_KEY", "AI21_API_KEY", "ANTHROPIC_API_KEY",
        "PINECONE_API_KEY", "SERPAPI_API_KEY", "TAVILY_API_KEY"
    ]
    
    key_name=''
    api_key = ''
    
    def __init__(self, key_name):
        self.key_name = key_name
        
        self.api_key = os.getenv(key_name)
        
        if not self.api_key:
            # Key not found in environment variables
            print("Key NOT found in environment.")
            print("Provide the ",key_name," : ")
            self.api_key=getpass.getpass()
            os.environ[key_name] = self.api_key
            print("Added key: ", key_name, " to the environment.")
        else:
            print("Key: ", key_name, " already set in environment.")

    def get_api_key(self):
        return self.api_key
