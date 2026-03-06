from data_fetcher import get_market_data
from market_agent import analyze_market

stocks = {
    "1": "MSFT",
    "2": "GOOGL",
    "3": "NVDA",
    "4": "TSLA",
    "5": "AAPL"
}

print("Select stock")

for k, v in stocks.items():
    print(k, v)

choice = input("Enter number: ")

ticker = stocks.get(choice)

if not ticker:
    print("Invalid choice")
    exit()

data = get_market_data(ticker)

result = analyze_market(data)

print(result)