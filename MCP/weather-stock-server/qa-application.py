#####################################################################
# Use the MCPStdioClient class defined in mcp_client_basic.py
# Implements the query loop that consist of the following steps
#   1. Get the query from the user
#       If query == exit end the loop
#       * Add the query to messages [role=user]
#   2. Invoke LLM with the query
#       * Add the response to the messages[role=system]
#   3. If LLM suggested a tool to be invoked invoke tool
#       * Add the response to messages [role=user]
#   4. Ask LLM to generate the final response
#####################################################################
import asyncio
from mcp_client_basic import MCPStdioClient

from openai import OpenAI
import os

from dotenv import load_dotenv
import json

from typing import List

# Load the file that contains the API keys - OPENAI_API_KEY
load_dotenv('C:\\Users\\raj\\.jupyter\\.env')


# Invokes the LLM
# You may switch the model to any of your choice
def llm_client(messages:List[str]):
    """
    Send a message to the LLM and return the response.
    """
    # Initialize the OpenAI client
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Send the message to the LLM
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        # messages=[{"role":"system",
        #             "content":"You are an intelligent assistant. You will execute tasks as prompted",
        #             "role": "user", "content": message}],
        messages = messages,
        max_tokens=250,
        temperature=0.2
    )

    # Extract and return the response content
    return response.choices[0].message.content.strip()

# Function to create a prompt from the query and tool info
def create_prompt_for_tool_selection(query, tools_info):
    system_prompt = f"""You are an expert in answering questions using the tools provided to you.
                        If you are unable to answer the question with available tools, respond with following format:
                        {{
                            "tool": "NO_TOOL_AVAILABLE"
                        }}
                        If you are able to answer the question using the tools, return the answer in the following format:
                        {{
                            "tool": "tool_name",
                            "arguments": {{
                                "argument-name": "value"
                            }}
                        }}
                        """
    prompt = f"""
    {system_prompt}
    Question: {query}
    Tools: {tools_info}
    """
    return prompt

# Function to create prompt with tool response
def create_prompt_with_tool_response(tool_response):
    prompt = f"""Use the tool response to generate your final response in plain text. If the tool="NO_TOOL_AVAILABLE" then response should say 
    
                'Sorry, no tool available to process your query!!'

                        {tool_response}
                        """
    return prompt

# Ask question - select tool - invoke tool - generate response
async def query_loop():

    # Create an instance of the MCP client
    client = MCPStdioClient("server.py")

    try:
        # Connect to the server & get the tools
        await client.connect_to_server()
        tools = await client.get_tools()
        # Create a string with info on all tools
        tools_info = "\n".join([f"- {tool.name}, {tool.description}, {tool.inputSchema} " for tool in tools.tools])

        # Create a loop that will take input from user & then generate the final response
        query = ""
        
        # Note: THIS IS NOT AN AGENTIC LOOP as only 1 tool can be called per query/cycle
        print("Starting query loop. To end, type 'exit' and hit <enter>")
        while query != "exit":

            messages = [
                            {
                                "role":"system",
                                "content":"You are an intelligent assistant. You will execute tasks as prompted"
                            }
            ]

            # 1. Get the query from user
            print("------------------------------------------------------------")
            query = input("Enter query: ")
            if query == "exit":
                break

            # 2. Create the prompt for tool selection - LLM will suggest a tool to be executed
            #    Then invoke the LLM
            prompt = create_prompt_for_tool_selection(query, tools_info)
            
            # 3. Add the query as user message
            messages.append({"role": "user", "content": prompt})
            llm_response = llm_client(messages)
            # print(f"LLM Response: {llm_response}")

            # Add response to messages
            messages.append({"role": "system", "content": llm_response})

            
            # 4. Call the tool if available
            tool_to_call = json.loads(llm_response)
            if tool_to_call["tool"] == "NO_TOOL_AVAILABLE":
                result = llm_response # "No tool available to answer the question"
            else:
                result = await client.call_tool(tool_to_call["tool"], tool_to_call["arguments"])
            
            # 5. Create prompt to generate the final response using the tool execution result
            prompt  = create_prompt_with_tool_response(result)
            messages.append({"role": "user", "content": prompt})

            # 6. Create final response
            llm_final_response = llm_client(messages)

            print(f"Result: {llm_final_response}")

            


    finally:
        # Without this you will get a Runtime exception
        await client.cleanup()




if __name__ == "__main__":
    # asyncio.run(create_session_get_tools())
    asyncio.run(query_loop())