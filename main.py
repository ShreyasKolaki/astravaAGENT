from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
from enum import Enum
from typing import List
from datetime import datetime

from data_fetcher import get_market_data
from market_agent import analyze_market
from social_sentiment_agent import analyze_social_sentiment
from financial_news_agent import fetch_financial_news

app = FastAPI(title="AI Stock Prediction API")


# ---------------------------------------
# STOCK ENUM (for dropdown control)
# ---------------------------------------
class StockName(str, Enum):
    microsoft = "microsoft"
    google = "google"
    nvda = "nvda"
    tsla = "tsla"
    aapl = "aapl"


# ---------------------------------------
# TICKER MAPPING
# ---------------------------------------
STOCK_TICKERS = {
    "microsoft": "MSFT",
    "google": "GOOGL",
    "nvda": "NVDA",
    "tsla": "TSLA",
    "aapl": "AAPL",
}


# ---------------------------------------
# RESPONSE MODELS (Matches Your UI)
# ---------------------------------------

class MarketResponse(BaseModel):
    stock: str
    ticker: str
    market_data: dict


class SentimentResponse(BaseModel):
    stock: str
    ticker: str
    prediction: dict


class NewsItem(BaseModel):
    title: str
    source: str
    published_at: datetime
    sentiment: str


class NewsResponse(BaseModel):
    stock: str
    ticker: str
    articles: List[NewsItem]


# ---------------------------------------
# HELPER
# ---------------------------------------
def get_ticker(symbol: str):
    symbol = symbol.lower()
    ticker = STOCK_TICKERS.get(symbol)
    if not ticker:
        raise HTTPException(status_code=404, detail="Stock not found")
    return symbol, ticker


# ---------------------------------------
# ROOT
# ---------------------------------------
@app.get("/")
def home():
    return {"message": "AI Stock Prediction API running 🚀"}


# ---------------------------------------
# MARKET ENDPOINT
# ---------------------------------------
@app.get("/agents/{symbol}/market", response_model=MarketResponse)
def market_endpoint(symbol: StockName):

    stock, ticker = get_ticker(symbol.value)

    try:
        market_data = get_market_data(ticker)

        return {
            "stock": stock,
            "ticker": ticker,
            "market_data": market_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------
# SENTIMENT ENDPOINT (AI Prediction)
# ---------------------------------------
@app.get("/agents/{symbol}/social-sentiment")
def social_sentiment_endpoint(symbol: StockName):

    stock, ticker = get_ticker(symbol.value)

    try:
        sentiment_data = analyze_social_sentiment(stock)

        return {
            "stock": stock,
            "ticker": ticker,
            "social_sentiment": sentiment_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------
# FINANCIAL NEWS ENDPOINT
# ---------------------------------------
@app.get("/agents/{symbol}/financial-news")
def financial_news_endpoint(symbol: StockName):

    stock, ticker = get_ticker(symbol.value)

    try:
        articles = fetch_financial_news(stock)

        return {
            "stock": stock,
            "ticker": ticker,
            "financial_news": articles
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------
# OPTIONAL: KEEP YOUR OLD /predict
# ---------------------------------------
class StockRequest(BaseModel):
    stock: StockName


@app.post("/predict")
def predict_stock(request: StockRequest):

    stock_name = request.stock.value
    ticker = STOCK_TICKERS.get(stock_name)

    if not ticker:
        raise HTTPException(status_code=400, detail="Invalid stock")

    try:
        market_data = get_market_data(ticker)
        prediction = analyze_market(market_data)

        return {
            "stock": stock_name,
            "ticker": ticker,
            "market_data": market_data,
            "prediction": prediction
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))