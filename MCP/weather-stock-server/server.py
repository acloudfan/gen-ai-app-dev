###################################################################################
# This MCP Server exposes dummy resources/tools to demonstrate the working of MCP #
# * Tool : Weather tool 
# * Tool : Stock
# * Resource : Cities
# * Resource : Stocks
# #################################################################################


# Import the FastMCP
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base
from typing import List
import time

# Create the MCP server
server_name = "Weather & Stock server"
mcp = FastMCP()

# Create an MCP tool for getting the stock price
@mcp.tool()
def  company_stock_price(stock_symbol: str) -> dict:
    """
    Retrieve the current stock price for a given company stock symbol.

    This function accepts a stock symbol and returns the current stock price for the specified company.
    It supports stock symbols for the following companies:
    - Apple Inc. ("AAPL")
    - Microsoft Corporation ("MSFT")
    - Amazon.com, Inc. ("AMZN")

    If the stock symbol does not match any of the supported companies, the function returns "unknown" as the price.

    Args:
        stock_symbol (str): The stock symbol of the company whose stock price is requested.

    Returns:
        dict: A dictionary containing the stock price with the key "price".
              If the stock symbol is not recognized, the value is "unknown".
    """
    if stock_symbol.upper()=='AAPL':
        return  {"price": 192.32}
    elif stock_symbol.upper()=='MSFT':
        return  {"price": 415.60}
    elif stock_symbol.upper()=='AMZN':
        return  {"price": 183.60}
    else:
        return {"price": "unknown"}


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

# Resource that simply returns the list of stocks supported by this server
@mcp.resource("stocks://")
def  supported_stocks()->List[str]:
    return ["AAPL", "MSFT","AMZN"]

# Resource that simply returns the list of stocks supported by this server
@mcp.resource("cities://")
def  supported_stocks()->List[str]:
    return ["new york", "paris","london"]


@mcp.prompt()
def  test_prompt_1()->str:
    prompt =    """
        I am interested in investing in one of these stocks: AAPL, MSFT, or AMZN.

        Decision Criteria:

        Sunny Weather: Choose the stock with the lowest price.
        Raining Weather: Choose the stock with the highest price.
        Cloudy Weather: Do not buy any stock.
        Location:

        I am currently in New York.
        Question:

        Based on the current weather in New York and the stock prices, which stock should I invest in?
    """
    return [base.UserMessage(prompt)]

@mcp.prompt()
def  test_prompt_2(location: str, budget: int)->str:
    return [
        base.UserMessage("""You are an expert in stocks.
                            I am interested in investing in one of these stocks: AAPL, MSFT, or AMZN.

                            Decision Criteria:

                            Sunny Weather: Choose the stock with the lowest price.
                            Raining Weather: Choose the stock with the highest price.
                            Cloudy Weather: Do not buy any stock."""),
        base.UserMessage(f"\nLocation: {location}\nBudget:{budget}"),
        base.UserMessage(f"which stock should I invest in?")
    ]


@mcp.tool()
async def  long_running_task_simulation(count_seconds: int, ctx: Context)->str:
    
    """Simulates long running task, progress returned every 1 second"""

    ctx.info("Long running task simulation started")
    for i in range(count_seconds):
        await ctx.report_progress(i, count_seconds)
        time.sleep(1)

    return f"Task completed in {count_seconds} seconds."



### Set transport=sse in the following code to launch the server with SSE endpoint ##
if __name__ == "__main__":
    mcp.run(transport='stdio') 