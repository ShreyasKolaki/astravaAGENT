from data_fetcher import get_market_data
from market_agent import analyze_market

stocks = {
    "1": "RELIANCE.NS",
    "2": "TCS.NS",
    "3": "NVDA",
    "4": "TSLA",
    "5": "AAPL"
}

print("Select stock")

for k,v in stocks.items():
    print(k,v)

choice = input("Enter number: ")

ticker = stocks[choice]

data = get_market_data(ticker)

result = analyze_market(data)

print(result)