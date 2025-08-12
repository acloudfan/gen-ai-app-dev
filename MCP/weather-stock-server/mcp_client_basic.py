# Import required modules
import asyncio
from mcp import ClientSession, StdioServerParameters  # MCP client components
from mcp.client.stdio import stdio_client  # STDIO transport implementation
from contextlib import AsyncExitStack  # For managing async resources

# Simple MCP client class for interacting with the MCP server via STDIO
class MCPStdioClient:
    # Class attributes (initialized as None)
    session = None,  # Will hold the ClientSession instance
    tools = None,    # Will cache available tools
    server_params = None  # Will store server connection parameters

    def __init__(self, server_script):
        """Initialize the client with server connection parameters.
        
        Args:
            server_script (str): Path to the server Python script to execute
        """
        # Configure how to launch the server process
        self.server_params = StdioServerParameters(
            command="python",  # Command to run the server
            args=[server_script]  # Arguments (the server script)
        )
        # Create an async context manager stack for resource cleanup
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self):
        """Establish connection to the MCP server via STDIO."""
        # Create STDIO transport and add to cleanup stack
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(self.server_params)
        )
        # Unpack the transport into read/write streams
        self.read, self.write = stdio_transport
        # Create ClientSession and add to cleanup stack
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.read, self.write)
        )
        # Initialize the MCP protocol session
        await self.session.initialize()
    
    async def get_tools(self):
        """Get list of available tools from the server."""
        return await self.session.list_tools()

    async def call_tool(self, tool_name, arguments):
        """Call a specific tool on the server with given arguments.
        
        Args:
            tool_name (str): Name of the tool to call
            arguments (dict): Arguments to pass to the tool
        """
        return await self.session.call_tool(tool_name, arguments)
    
    async def cleanup(self):
        """Clean up all resources and connections."""
        await self.exit_stack.aclose()

async def basic_example():
    """Demonstrate basic usage of the MCP client."""
    # Create client instance pointing to our server script
    client = MCPStdioClient("server.py")

    try:
        # Connect to the server
        await client.connect_to_server()
        
        # Get and display available tools
        tools = await client.get_tools()
        print("Available Tools:")
        for i, tool in enumerate(tools.tools):
            print(f"Tool#{i}: {tool.name}, {tool.description}, {tool.inputSchema}")

        # Call some example tools and show results
        print("\nCalling Tools:")
        print("-------------------------------------")
        result = await client.call_tool("company_stock_price", {"stock_symbol": "AAPL"})
        print("Stock Price Result:", result)
        print("-------------------------------------")
        
        result = await client.call_tool("city_weather", {"city": "new york"})
        print("Weather Result:", result)
        print("-------------------------------------")
    finally:
        # Ensure proper cleanup even if errors occur
        await client.cleanup()
    
if __name__ == "__main__":
    # Run the example using asyncio
    asyncio.run(basic_example())