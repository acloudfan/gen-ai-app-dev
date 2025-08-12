# This sample code demonstrates the use of MCP tools use from a "Tool calling agent"
# Code is using the Langchain MCP adapter library and Open AI model
# uv add langchain langchain-adapters langchain-openai
# https://python.langchain.com/api_reference/langchain/agents/langchain.agents.tool_calling_agent.base.create_tool_calling_agent.html
# https://github.com/langchain-ai/langchain-mcp-adapters

from openai import OpenAI
from langchain_openai import ChatOpenAI
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_mcp_adapters.tools import load_mcp_tools

import pathlib

from dotenv import load_dotenv

# Load the file that contains the API keys - OPENAI_API_KEY
load_dotenv('C:\\Users\\raj\\.jupyter\\.env')


mcp_server_folder = pathlib.Path(__file__).parent.resolve()
server_params = StdioServerParameters(
    command="uv",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["run", f"{mcp_server_folder}/mcp-server-stock.py"],
)

# 1. Setup the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. You would use the provided tools to answer the question."),

        ("human", "{question}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# 2. Setup the LLM - you will get an error if a valid key is not provided
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")

# 3. Create a tool calling agent to answer a question
# Gets the MCP tools, converts the tools to StructuredTool 
async def query_with_tools(llm, prompt, question):
# Create the ClientSession & get tools
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Initialize the connection
            await session.initialize()

            # Get MCP tools & convert to LangChain StructuredTool
            tools = await load_mcp_tools(session)

            # Create the tool calling agent
            agent = create_tool_calling_agent(llm, tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
            response = await agent_executor.ainvoke({"question": question})

            print(response)


# Test
question = "what is the price of apple stock"

agent = asyncio.run(query_with_tools(llm, prompt, question))

