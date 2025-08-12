# Demonstrates the working of MultiServerMCPClient
#### LangChain MCP adapter https://github.com/langchain-ai/langchain-mcp-adapters
#### LangGraph MultiServerMCPClient https://langchain-ai.github.io/langgraph/reference/mcp/#langchain_mcp_adapters.client.MultiServerMCPClient

# from mcp import ClientSession
import pathlib
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI


from dotenv import load_dotenv

# 1.Load the file that contains the API keys - OPENAI_API_KEY
load_dotenv('C:\\Users\\raj\\.jupyter\\.env')

# 2. Setup the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. You would use the provided tools to answer the question."),

        ("human", "{question}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# 3. Setup the multi server client
current_script_folder = pathlib.Path(__file__).parent.resolve()
print(current_script_folder)
client = MultiServerMCPClient(
    {
        "weather": {
            "command": "uv",
            "args": ["run", f"{current_script_folder}/mcp-server-weather.py"],
            "transport": "stdio",
        },
        "stock": {
            "command": "uv",
            "args": ["run", f"{current_script_folder}/mcp-server-stock.py"],
            "transport": "stdio",
        }
    }
)

# 4. Get the tools
tools = asyncio.run(client.get_tools())

# 5. Create a tool calling agent
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
tool_calling_agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=tool_calling_agent, tools=tools, verbose=True)

# Test
question = "hows is the weather in NYC"
question = "should i buy AAPL?"
response = asyncio.run(agent_executor.ainvoke({"question": question}))
print(response)