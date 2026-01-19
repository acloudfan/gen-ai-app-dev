# Industry news research agent
# Agent carries out the websearch to find news articles on the specified industry.
# It uses the content of the articles to generate an industry outlook report.

# TOOL
# ```uv add langchain-tavily```
# ```%pip install -qU langchain-tavily```
# https://python.langchain.com/docs/integrations/tools/tavily_search/
# https://python.langchain.com/docs/integrations/tools/#search

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from typing import List
from pydantic import BaseModel, Field
from enum import Enum

# Tool for the agent
from langchain_tavily import TavilySearch

# Stock outlook decision
class DecisionEnum(str, Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    
# Structured output format
class IndustryNewsResearchReport(BaseModel):
    decision: DecisionEnum = Field(
        ...,
        description="Decision on whether to 'BUY', 'HOLD', or 'SELL' stock"
    )
    report: str = Field(
        ...,
        description="A concise summary for the stock outlook based on the latest news."
    )
    reasons: List[str] = Field(
        ...,
        description="List of supporting reasons or factors that justify the report"
    )
    industry: str = Field(
        ...,
        description="Company's industry."
    )
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for the recommendation, ranging from 0 (low confidence) to 1 (high confidence)"
    )

# Create the agent
def create_industry_research_agent(chat_llm, name = "industry-news-research-agent"):

    """Creates and configures an industry research agent for stock trend analysis.
    
    This agent specializes in analyzing industry sector trends by examining major reports
    and projecting their impact on company stocks within that industry. The agent utilizes
    web search capabilities to gather recent industry news and generates structured research
    reports.

    Args:
        chat_llm: The language model instance that will power the agent's reasoning capabilities.
        name (str, optional): The name identifier for the agent. Defaults to "industry-news-research-agent".

    Returns:
        Agent: A configured reactive agent capable of:
               - Identifying a company's industry sector from its ticker symbol
               - Researching recent industry trends through web search
               - Analyzing the potential impact on company stocks
               - Generating structured research reports

    The agent is configured with:
        - A specialized prompt defining its industry analysis expertise
        - Tavily web search tool (limited to 5 recent news results from past month)
        - Structured response format using IndustryNewsResearchReport

    Example:
        >>> research_agent = create_industry_research_agent(llm_instance)
        >>> report = research_agent.run("AAPL")
    """

    # prompt = """You are an expert in understanding the stock trends in a given industry sector. 
    #             You do this by analyzing major reports about the specified industry. 
    #             Based on your analysis you project the impact on stocks of those companies in the industry.
    #             You will be given a stock ticker symbol or the industry sector to research.
    #             If you are asked to analyze the stock ticker,  start by getting the stock's industry sector followed by providing a decision to BUY, SELL or HOLD the stock."""

    prompt = """
        You are an expert in understanding the stock trends in a given industry sector.
        
        Analyze the major reports about the specified industry and provide a JSON object exactly matching this schema:
        
        {
          "report": string,
          "industry": string,
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

    web_search_with_tavily = TavilySearch(
        max_results=5,
        topic="news",
        time_range="month"
    )
    
    # Create the agent
    agent = create_react_agent(
        model = chat_llm,
        tools = [web_search_with_tavily],
        name = name,
        prompt = prompt,
        response_format = IndustryNewsResearchReport
    )

    return agent

def get_agent_card():
    agent_card = {
      "name": "industry-news-research-agent",
      "description": "A specialized agent for analyzing industry sector trends and projecting their impact on company stocks.",
      "capabilities": {
        "analysis_type": "Industry trend impact analysis",
        "output_format": "Structured research report with industry classification",
        "focus_area": "Macro-level industry trends affecting stock performance"
      },
      "input_requirements": {
        "required_input": "Stock ticker symbol (e.g., 'AAPL')",
        "optional_inputs": [
          "Specific research query (e.g., 'Impact of AI regulations on semiconductor stocks')"
        ]
      },
      "output_specification": {
        "format": "JSON",
        "schema": {
          "report": {
            "type": "string",
            "description": "Concise summary of the stock outlook based on industry trends"
          },
          "reasons": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "Key factors supporting the analysis (e.g., regulatory changes, market trends)"
          },
          "industry": {
            "type": "string",
            "description": "Identified industry sector of the company"
          },
          "confidence_score": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "Confidence in the projected impact (0=low, 1=high)"
          }
        }
      },
      "usage_notes": {
        "best_for": "Macro-level analysis of how industry trends affect specific stocks",
        "limitations": [
          "Does not perform company-specific fundamental analysis",
          "Relies on recent news (past month) for trend detection"
        ],
        "confidence_guidelines": {
          "high": ">0.8 - Strong consensus in industry reports",
          "medium": "0.5-0.8 - Mixed signals with dominant trend",
          "low": "<0.5 - Limited or conflicting industry data"
        },
        "example_use_cases": [
          "Assessing how supply chain disruptions affect automotive stocks",
          "Projecting the impact of ESG policies on energy sector valuations",
          "Analyzing tech industry hiring trends for growth signals"
        ]
      }
    }

    return agent_card
# Unit test code
if __name__ == "__main__":
    print("hello World")
