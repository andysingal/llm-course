import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

def get_openai_api_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key

def get_tavily():
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    tavily_client = TavilyClient(api_key=tavily_api_key)
    return tavily_client





