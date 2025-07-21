# This is a dummy MCP server that exposes a single tool
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base
from typing import List
import time

# Create the MCP server
server_name = "Stock server"
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


# Run server with stdio
if __name__ == "__main__":
    mcp.run(transport='stdio')