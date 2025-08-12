# https://medium.com/@sajith_k/creating-an-mcp-server-and-integrating-with-langgraph-5f4fa434a4c7

# MCP tools
# Demonstrates how the ToolNode can connect to MCP servers for invoking the tools, access the resources, and prompts.
# 1. Create an MCP session to 2 MCP servers
# 2. Create a graph with ToolNode
# 3. Use the MultiServerMCP client from ToolNode to interact with servers
#### LangChain MCP adapter https://github.com/langchain-ai/langchain-mcp-adapters
#### LangGraph MultiServerMCPClient https://langchain-ai.github.io/langgraph/reference/mcp/#langchain_mcp_adapters.client.MultiServerMCPClient

import pathlib
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import ToolNode
import asyncio
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import AIMessage


# 1. Create the MultiServerMCPClient
async def create_mcp_client() :

    # get the folder for this script
    current_script_folder = pathlib.Path(__file__).parent.resolve()
    print(current_script_folder)
    client = MultiServerMCPClient(
        {
            "weather": {
                "command": "uv",
                "args": ["run", f"{current_script_folder}/mcp/mcp-server-weather.py"],
                "transport": "stdio",
            },
            "stock": {
                "command": "uv",
                "args": ["run", f"{current_script_folder}/mcp/mcp-server-stock.py"],
                "transport": "stdio",
            }
        })
    # Unit testing
    # response = await tools[0].ainvoke({"city": "new york"})
    # print("RESPONSE=",response)
    return client


# 2. Tool Node
async def create_tool_node(client):

    # Get the tools from the MCP servers using the client
    tools = await client.get_tools()

    # print(tools)
    tool_node = ToolNode(
        name = "tool_node",
        tools = tools,
        handle_tool_errors = True
    )
    return tool_node

# 3. Create the graph with a single node
#    - Calls: create_mcp_client() to create an MCP client
#    - Calls: create_tool_node() to setup a ToolNode with MCP server tools
#    Sets up the graph : Start -> Tool node -> End
#    Uses the MessagesState as the state schema
async def create_graph():
    # Create the MultiServerMCPClient
    client = await create_mcp_client()
    tool_node = await create_tool_node(client)

    # Create the graph
    # Create the state graph builder
    workflow_builder = StateGraph(MessagesState)

    # workflow_builder.add_node("llm_simulation", llm_simulation)
    workflow_builder.add_node("tool_node", tool_node)
    # workflow_builder.add_edge(START, "llm_simulation")
    workflow_builder.add_edge(START, "tool_node")
    # workflow_builder.add_edge("llm_simulation", "tool_node")
    workflow_builder.add_edge("tool_node", END)

    # Compile the graph
    workflow_compiled = workflow_builder.compile()

    return workflow_compiled

# Setup & test
async def main():
    # Create the graph
    workflow_compiled = await create_graph()

    # LLM Simulaton : Add one or more tool calls
    messages = AIMessage(
        content = "dummy",
        tool_calls = [
            {"name": "city_weather", "args": {"city": "Paris"}, "id": "dummy"},
            {"name": "company_stock_price", "args": {"stock_symbol": "AMZN"}, "id": "dummy"}
        ]
    )

    # Invoke the workflow
    response =  await workflow_compiled.ainvoke({"messages": [messages]})

  
    # Read the ToolMessages after the AI message
    for message in reversed(response["messages"]):
        if isinstance(message,AIMessage):
            break
        print(message.content)


if __name__ == "__main__":
    # Run the example using asyncio
    response = asyncio.run(main())
