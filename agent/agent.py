import os
import certifi
import ssl
from dotenv import load_dotenv
from urllib.request import urlopen


from google.adk.agents import Agent
from google.adk.tools import ToolContext

from typing import Optional, Dict, Anyv


MODEL_ID = os.getenv("GENAI_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = """You are a Financial Analysis Agent

You source financial information from APIs and perform analysis on the financial data for S&P 500.

"""


def fmp_cashflow_statement(tool_context: ToolContext, ticker: str) -> Optional[str]:
    """Hits the FMP API to retrieve the cash flow information for the company with the given ticker.

    Args:
        ticker: The ticker of the company we want to access the balance sheet

    Returns:
        A formatted string with search results, or None if no results.
    """
    url = (f"https://financialmodelingprep.com/stable/cash-flow-statement-as-reported?symbol={ticker}&apikey={os.getenv('FMP_KEY')}")
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        response = urlopen(url, context=context)
        data = response.read().decode("utf-8")
        return data
    except Exception as e:
        logger.error(f"fmp API request for cash flow statement informaation failed for {ticker}")



def create_agent() -> Agent:
    """Create ADK Agent with all tools"""
    return Agent(
        name="financial_planning_agent",
        model=MODEL_ID,
        instruction=SYSTEM_PROMPT,
        tools=[fmp_cashflow_statement
        ],

    )