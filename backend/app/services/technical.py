import pandas as pd
import yfinance as yf

def get_technical_indicators(symbol):
    stock = yf.Ticker(symbol)
    df = stock.history(period="6mo")

    # Moving averages
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()

    # RSI calculation
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    latest = df.iloc[-1]

    return {
        "price": float(latest["Close"]),
        "MA20": float(latest["MA20"]),
        "MA50": float(latest["MA50"]),
        "RSI": float(latest["RSI"])
    }