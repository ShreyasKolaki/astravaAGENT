import yfinance as yf


def get_market_data(ticker: str) -> dict:

    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")

    if hist.empty:
        raise ValueError("No data found for ticker")

    current_price = float(hist["Close"].iloc[-1])
    ema20 = float(hist["Close"].ewm(span=20).mean().iloc[-1])
    ema50 = float(hist["Close"].ewm(span=50).mean().iloc[-1])
    volume = int(hist["Volume"].iloc[-1])

    # Optional: price history for chart
    price_history = hist["Close"].tolist()
    volume_history = hist["Volume"].tolist()

    return {
        "current_price": current_price,
        "ema_20": ema20,
        "ema_50": ema50,
        "volume": volume,
        "price_history": price_history,
        "volume_history": volume_history
    }