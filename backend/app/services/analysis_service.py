import yfinance as yf
import pandas as pd

def moving_average(symbol):

    stock = yf.Ticker(symbol)

    hist = stock.history(period="3mo")

    hist["MA20"] = hist["Close"].rolling(window=20).mean()

    data = hist.tail(5)[["Close","MA20"]]

    return data.reset_index().to_dict(orient="records")