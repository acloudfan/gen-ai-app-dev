# This is a dummy MCP server that exposes a single tool
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base
from typing import List
import time

# Create the MCP server
server_name = "Weather server"
mcp = FastMCP()

# Create an MCP tool for getting the city weather
@mcp.tool()
def city_weather(city: str) -> dict:
    """
    Retrieve the current weather information for a given city.

    This function accepts a city name and returns a dictionary containing the current temperature and weather forecast for that city. 
    It supports the following cities:
    - New York
    - Paris
    - London

    If the city is not recognized, the function returns "unknown" for the temperature.

    Args:
        city (str): The name of the city for which the weather information is requested.

    Returns:
        dict: A dictionary with the following keys:
            - "temperature": The current temperature in Fahrenheit.
            - "forecast": A brief description of the current weather forecast.
            
        If the city is not recognized, the "temperature" key will have a value of "unknown".
    """
    if city.lower() == "new york":
        return {"temperature": 68, "forecast": "rain"}
    elif city.lower() == "paris":
        return {"temperature": 73, "forecast": "sunny"}
    elif city.lower() == "london":
        return {"temperature": 82, "forecast": "cloudy"}
    else:
        return {"temperature": "unknown"}

# Run server with stdio
if __name__ == "__main__":
    mcp.run(transport='stdio') 