```py
import re

import pandas as pd
import streamlit as st
import yfinance as yf
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph_swarm import create_handoff_tool, create_swarm
from pycoingecko import CoinGeckoAPI

model = ChatOllama(model="qwen3:8b", temperature=0.1)

stock_advisor_prompt = (
    "You are a stock investment advisor.\n\n"
    "INSTRUCTIONS:\n"
    "- Use the provided tools: fetch_stock_info"
    "- The input to these tools should be a stock symbol like 'AAPL' or 'GOOGL'.\n"
    "- When asked about a specific stock or company:\n"
    "  • Retrieve general information like its name, sector, and market cap.\n"
    "  • Analyze quarterly and annual financials (focus on Total Revenue and Net Income).\n"
    "  • Review price trends over the past year.\n"
    "- If the question is about **cryptocurrencies** (e.g., Bitcoin, Ethereum, Solana), "
    "use the transfer tool to hand off to the crypto advisor agent immediately.\n"
    "- Provide clear, objective, data-driven insights to support investment decisions.\n"
    "- Do NOT give disclaimers, speculation, or refer users to external sources.\n"
    "- Use ONLY the available tool outputs to form your response."
)

crypto_advisor_prompt = (
    "You are the active cryptocurrency investment advisor agent.\n\n"
    "You have received a user query that is specifically about cryptocurrencies.\n"
    "Your job is to analyze and respond directly using the tools provided.\n\n"
    "INSTRUCTIONS:\n"
    "- Use the provided tools: fetch_coin_info.\n"
    "- The input of the tools should be the coin ID (e.g., 'bitcoin', 'solana'), all in lower case.\n"
    "- When asked about a cryptocurrency:\n"
    "  • Explain the coin’s purpose using its description.\n"
    "  • Provide key metrics such as market cap and rank.\n"
    "  • Analyze the price history over the past year to identify trends or volatility.\n"
    "- If the question is about **stocks, ETFs, or traditional financial markets**, "
    "use the transfer tool to hand off to the stock advisor agent immediately.\n"
    "- Do NOT try to answer stock-related questions yourself.\n"
    "- Do NOT give disclaimers, opinions, or refer users elsewhere.\n"
    "- Base your entire response strictly on the data returned by the tools."
)

def clean_text(text: str):
    cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return cleaned_text.strip()

@tool
@st.cache_data
def fetch_stock_info(symbol: str):
    """Get Company's general information. Input should be the stock symbol, e.g., 'AAPL'."""
    stock = yf.Ticker(symbol)

    annual_financials = stock.financials.T[['Total Revenue', 'Net Income']].round(2)
    annual_financials.index = annual_financials.index.strftime('%Y-%m-%d')

    price_history = stock.history(period='1y', interval='1d').reset_index()
    price_history['Date'] = pd.to_datetime(price_history['Date']).dt.date
    price_history = price_history.round(2)

    return {
        "symbol": symbol,
        "annual_financials": annual_financials.to_dict(orient='index'),
        "min_price_last_year": round(price_history['Close'].min(), 2),
        "max_price_last_year": round(price_history['Close'].max(), 2),
        "average_price_last_year": round(price_history['Close'].mean(), 2),
        "current_price": round(price_history['Close'].iloc[-1], 2)
    }

@tool
@st.cache_data
def fetch_coin_info(coin_id: str):
    """Get cryptocurrency general information. Input should be the coin's ID, e.g., 'bitcoin'."""
    cg = CoinGeckoAPI()
    coin_info = cg.get_coin_by_id(coin_id)
    price_history = cg.get_coin_market_chart_by_id(coin_id, vs_currency='usd', days=365)
    prices = [entry[1] for entry in price_history["prices"]]

    return {
        "description": coin_info['description']['en'],
        "market_cap_usd": coin_info['market_data']['market_cap']['usd'],
        "market_cap_rank": coin_info['market_cap_rank'],
        "min_price_last_year": round(min(prices), 2),
        "max_price_last_year": round(max(prices), 2),
        "average_price_last_year": round(sum(prices) / len(prices), 2),
        "current_price": round(prices[-1], 2)
    }

stock_advisor = create_react_agent(
    model,
    tools=[
        fetch_stock_info,
        create_handoff_tool(
            agent_name="crypto_advisor",
            description="Use this tool to transfer any queries about the cryptocurrencies like Bitcoin, Ethereum, Solana, etc."
        )
    ],
    name="stock_advisor",
)

crypto_advisor = create_react_agent(
    model,
    tools=[
        fetch_coin_info,
        create_handoff_tool(
            agent_name="stock_advisor",
            description="Use this tool to transfer any queries about the stocks like Apple, Tesla, Microsoft, etc."
        )
    ],
    name="crypto_advisor",
)

workflow = create_swarm(
    agents=[stock_advisor, crypto_advisor],
    default_active_agent="stock_advisor"
)

app = workflow.compile()

query = st.text_input("Enter your investment inquiry:")

if query:
    config = {"configurable": {"thread_id": "1"}}
    result = app.invoke({
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })

    for message in result["messages"]:
        print(message.pretty_print())
        print()

    response = clean_text(result["messages"][-1].content)
    st.markdown(response)
```

### requirements.txt
```py
streamlit
langchain_core
langchain_community
langchain_ollama
langgraph
langgraph-swarm
pycoingecko
yfinance
```
