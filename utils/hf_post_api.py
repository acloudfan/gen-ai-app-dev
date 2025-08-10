# Use the model API endpoint to invoke the model
# https://huggingface.co/docs/api-inference/detailed_parameters#text-generation-task
# Note:
# If the requested model is not loaded in memory, the Serverless Inference API will start by loading the model into memory and returning a 503 response, before it # can respond with the prediction.
# Invocation parameters
#  - String input & output
#  - Task specific
# Checkout list of models by opening the link in browser : https://router.huggingface.co/v1/models
#
# AUG 10th, 2025
# HF NO MORE SUPPORT DIRECT HTTP ENDPOINT Invocation - Replacing with InferenceClient()

import requests
import getpass
import os
from huggingface_hub import InferenceClient

class hf_rest_client:
    # Holds the model to be invoked
    model_api_url = ""
    
    # Holds the API token
    HUGGINGFACEHUB_API_TOKEN=""

    # Initialize
    def  __init__(self, model_id, api_token=None):

        # Check if API token is provided, if not then check env, if not ask for it
        if not api_token:
            self.HUGGINGFACEHUB_API_TOKEN=os.getenv('HUGGINGFACEHUB_API_TOKEN')
            if not self.HUGGINGFACEHUB_API_TOKEN:
                print("Provide the HUGGINGFACEHUB_API_TOKEN:")
                self.HUGGINGFACEHUB_API_TOKEN=getpass.getpass()
        else:
            self.HUGGINGFACEHUB_API_TOKEN=api_token
            
        self.model_id=model_id
        # root URL is the same for all models invocation endpoints
        self.model_api_url = "https://api-inference.huggingface.co/models/"+model_id
        self.inference_client = InferenceClient(model=model_id,
                                                # provider = "hf-inference",
                                                token = self.HUGGINGFACEHUB_API_TOKEN
                                               )

    # Returns the model's API URL
    def get_model_url(self):
        return self.model_api_url

    def invoke(self, query, parameters = {}, options={}):
        messages = [{"role": "user", "content": query}]
        response = self.inference_client.chat_completion(messages, max_tokens=100)
        return response.choices[0].message.content
        

  
    # Invoke function
    # def invoke(self, query, parameters = {}, options={}):

    #     # Setup header with API token
    #     headers = {"Authorization": f"Bearer {self.HUGGINGFACEHUB_API_TOKEN}"}

    #     # Create the payload JSON
    #     payload =  {
    #         "inputs": query,
    #         "parameters": parameters,
    #         "options": options
    #     }

    #     # print(payload)
    #     print(self.model_api_url)

    #     # Post to the model URL
    #     response = requests.post(self.model_api_url, headers=headers, json=payload)

    #     # Check for errors
    #     if response.status_code != 200:
    #         # error !!
    #         return {
    #             "status_code": response.status_code,
    #             "reason" : response.reason,
    #             "error": True
    #         }
    #     else:
    #         # Return response as JSON
    #         return response.json()


# Unit test case : Aug 10, 2025
# llm_client = hf_rest_client("meta-llama/Meta-Llama-3-8B-Instruct")
# text="capital of india"
# response = llm_client.invoke(text)
# print(response)