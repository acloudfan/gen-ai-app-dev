# LangChain MCP adapters library
# https://github.com/langchain-ai/langchain-mcp-adapters
# uv add langchain-mcp-adapters
# StructuredTool = https://python.langchain.com/api_reference/core/tools/langchain_core.tools.structured.StructuredTool.html
# This sample code simply dumps the information about the tools available in a single MCP server.
# LangChain MultiServerMCP client allows you to configure a single client for multiple MCP server
# https://github.com/langchain-ai/langchain-mcp-adapters?tab=readme-ov-file#client-1

# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import pathlib
from langchain_mcp_adapters.tools import load_mcp_tools



mcp_server_folder = pathlib.Path(__file__).parent.resolve()
server_params = StdioServerParameters(
    command="uv",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["run", f"{mcp_server_folder}/mcp-server-stock.py"],
)

async def main():
    # The session will be automatically closed as soon as the execution exits this block
    # Use of session outside this block, will result in an error: connection closed
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)
            # print(tools)

            print("Available Tools:")
            for tool in tools:
                print(f"{tool.name}\n {tool.description}\n {tool.args_schema=}")
                print("------------------------------------------------------------------")

            # return the tools
            return tools
        

if __name__ == "__main__":
    # Run the example using asyncio
    asyncio.run(main())


