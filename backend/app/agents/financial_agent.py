from app.services.technical import get_technical_indicators
from app.services.news import get_news_sentiment

def analyze_stock(symbol):

    tech = get_technical_indicators(symbol)

    sentiment = get_news_sentiment(symbol.split(".")[0])

    trend = "Bullish" if tech["price"] > tech["MA50"] else "Bearish"

    report = f"""
Financial Research Report

Stock: {symbol}

Current Price: {tech['price']}

Technical Indicators
MA20: {tech['MA20']}
MA50: {tech['MA50']}
RSI: {tech['RSI']}

Trend: {trend}

News Sentiment: {sentiment}

Conclusion:
This stock shows a {trend} technical structure with {sentiment} media sentiment.

Disclaimer: This is not investment advice.
"""

    return report