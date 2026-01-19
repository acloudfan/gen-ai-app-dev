# Stock news research agent
# Agent uses the Yahoo Finance New API to get the news for the given article
# It uses the content of the article to generate a stock outlook report.

# TOOL package dependency
# This agent needs a finance news search tool. We will use Yahoo Finance search for this. 
# ```pip install --upgrade --quiet  yfinance```
# ```uv add yfinance```
# https://python.langchain.com/docs/integrations/tools/yahoo_finance_news/
# https://algotrading101.com/learn/yahoo-finance-api-guide/

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from typing import List
from pydantic import BaseModel, Field
from enum import Enum

from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool

# Stock outlook decision
class DecisionEnum(str, Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    
# Structured output format
class StockNewsResearchReport(BaseModel):
    report: str = Field(
        ...,
        description="A concise summary for the stock outlook based on the latest news."
    )
    reasons: List[str] = Field(
        ...,
        description="List of supporting reasons or factors that justify the report"
    )
    decision: DecisionEnum = Field(
        ...,
        description="Final decision: BUY, HOLD, or SELL"
    )
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for the recommendation, ranging from 0 (low confidence) to 1 (high confidence)"
    )

# Create the agent
def create_stock_research_agent(chat_llm,  name = "stock-news-research-agent"):

    """Creates a specialized agent for researching stock news and generating impact reports.

    This agent is designed to analyze financial news and generate reports about their potential
    impact on stock prices. It utilizes the Yahoo Finance news tool to gather relevant information.

    Args:
        chat_llm: The language model instance that will power the agent's reasoning capabilities.
        name (str, optional): The name identifier for the agent. Defaults to "stock-news-research-agent".

    Returns:
        Agent: A configured react agent instance specialized for stock news research with:
            - Access to Yahoo Finance news data
            - Ability to generate stock impact reports
            - Custom prompt for financial analysis

    Example:
        >>> llm = ChatOpenAI(model="gpt-4")
        >>> agent = create_stock_research_agent(chat_llm=llm)
        >>> report = agent.run("Analyze the impact of Apple's earnings report on its stock")
    """

    prompt = """You are an expert in understanding the impact of various events on stocks. 
                You use the tools to gather information about stock and use this information 
                to generate a short report on its impact on the stock price."""

    # Financial news tool
    stock_news_tool = YahooFinanceNewsTool()
    
    # Create the agent
    agent = create_react_agent(
        model = chat_llm,
        tools = [stock_news_tool],
        name = name,
        prompt = prompt,
        response_format = StockNewsResearchReport
    )

    return agent

def  get_agent_card():
    agent_card = {
          "name": "stock-news-research-agent",
          "description": "A specialized agent for analyzing financial news and generating reports about their potential impact on stock prices.",
          "capabilities": {
            "analysis_type": "Stock news impact analysis",
            "output_format": "Structured research report with confidence scoring",
            "focus_area": "Event-driven stock price impact"
          },
          "input_requirements": {
            "required_input": "Stock-related query or news topic",
            "input_examples": [
              "Analyze the impact of Apple's earnings report on its stock",
              "How will the new FDA approval affect Pfizer's stock price?"
            ]
          },
          "output_specification": {
            "format": "JSON",
            "schema": {
              "report": {
                "type": "string",
                "description": "Concise summary of the stock outlook based on latest news"
              },
              "reasons": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Supporting reasons/factors justifying the report"
              },
              "confidence_score": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0,
                "description": "Confidence in the recommendation (0=low, 1=high)"
              }
            }
          },
          "usage_notes": {
            "best_for": "Analyzing how recent news/events might affect stock prices",
            "limitations": "Does not incorporate technical analysis or historical price trends",
            "confidence_interpretation": {
              "high": ">0.75 - Strong evidence supporting the conclusion",
              "medium": "0.5-0.75 - Moderate evidence with some uncertainty",
              "low": "<0.5 - Tentative conclusion based on limited information"
            },
            "typical_use_cases": [
              "Earnings report analysis",
              "Regulatory impact assessment",
              "Product launch evaluations",
              "Merger/acquisition impact studies"
            ]
          }
    }
    return agent_card

    
# Unit test code
if __name__ == "__main__":
    print("hello World")
