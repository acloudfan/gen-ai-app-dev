# Stock performance analysis
# Agent uses the Yahoo Finance API to get the news stock trend

# Tools
# ```pip install --upgrade --quiet  yfinance```
# ```uv add yfinance```
# https://python.langchain.com/docs/integrations/tools/yahoo_finance_news/
# https://algotrading101.com/learn/yahoo-finance-api-guide/

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from typing import List
from pydantic import BaseModel, Field
from enum import Enum

from langchain_core.tools import tool
import yfinance as yf

# Stock outlook decision
class DecisionEnum(str, Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"

# Structured output format
class StockTrendAnalysis(BaseModel):
    analysis: str = Field(
        ...,
        description="A concise analysis for the stock's outlook based on the stock's price history."
    )
    reasons: List[str] = Field(
        ...,
        description="List of supporting reasons or factors that justify the analysis"
    )
    decision: DecisionEnum = Field(
        ...,
        description="Final decision for the stock: BUY or HOLD or SELL"
    )
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for the prediction, ranging from 0 (low confidence) to 1 (high confidence)"
    )

def stock_history_tool(ticker_symbol):
    """
      This tools provides the stock history data.
    """
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="max")

    return data

# Create the agent
def create_stock_trend_analyst_agent(chat_llm, name = "stock-trend-analyst-agent"):

    """Creates a specialized agent for analyzing and predicting stock price trends.

    This function configures and returns an agent that is expert in analyzing historical
    stock price data to predict future price movements (higher, lower, or stable).

    Args:
        chat_llm: The language model instance that will power the agent's reasoning capabilities.
        name (str, optional): The name identifier for the agent. Defaults to 
            "stock-trend-analyst-agent".

    Returns:
        An agent instance configured with:
        - Stock price analysis expertise
        - Access to stock history data tools
        - Structured response format for trend analysis

    The agent is pre-configured with:
        - A specialized prompt framing its expertise
        - The stock_history_tool for accessing historical data
        - StockTrendAnalysis as its response format
    """

    # prompt = """You are an expert in analyzing the stock price trends. You review the stock price history to predict whether the stock price will 
    #             be lower, higher or stay the same in near future. You MUST provide a decision on whether to BUY, HOLD or SELL the stock.
    #             You assign a confidence score to your recommendation between 0 and 1"""

    prompt = """
        You are an expert financial analyst analyzing stock price trends.
        
        Analyze the stock's historical prices and provide a JSON object exactly matching this schema:
        
        {
          "analysis": string,
          "reasons": string[],
          "decision": "BUY" | "HOLD" | "SELL",
          "confidence_score": number (0.0 to 1.0)
        }
        
        Rules:
        - All fields are mandatory.
        - "decision" must be exactly one of: BUY, HOLD, SELL (uppercase, no extra spaces)
        - Do not include any text outside the JSON
        - Even if uncertain, you must choose one of BUY, HOLD, SELL
        """

    
    # Create the agent
    agent = create_react_agent(
        model = chat_llm,
        tools = [stock_history_tool],
        name = name,
        prompt = prompt,
        response_format = StockTrendAnalysis,
        debug=False
    )

    return agent

def get_agent_card():
    agent_card = {
          "name": "stock-trend-analyst-agent",
          "description": "A specialized agent for analyzing and predicting stock price trends based on historical data.",
          "capabilities": {
            "analysis_type": "Stock price trend prediction",
            "output_format": "Structured analysis with confidence scoring",
            "time_horizon": "Near future outlook"
          },
          "input_requirements": {
            "required_input": "Stock ticker symbol",
            "optional_inputs": []
          },
          "output_specification": {
            "format": "JSON",
            "schema": {
              "analysis": {
                "type": "string",
                "description": "Concise analysis of the stock's outlook (higher, lower, or stable)"
              },
              "reasons": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Supporting reasons/factors justifying the analysis"
              },
              "confidence_score": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0,
                "description": "Confidence in the prediction (0=low, 1=high)"
              }
            }
          },
          "usage_notes": {
            "best_for": "Preliminary stock trend analysis based on price history",
            "limitations": "Does not incorporate fundamental analysis or external market factors",
            "confidence_thresholds": {
              "high": ">0.7",
              "medium": "0.4-0.7",
              "low": "<0.4"
            }
          }
    }

    return agent_card

# Unit test code
if __name__ == "__main__":
    print("hello World")
