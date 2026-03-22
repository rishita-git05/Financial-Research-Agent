from app.services.technical import get_technical_indicators
from app.services.news import get_news_sentiment

def analyze_stock(symbol):

    # 🔹 Step 1: Fetch data
    tech = get_technical_indicators(symbol)
    sentiment = get_news_sentiment(symbol.split(".")[0])

    # 🔹 Step 2: Derived logic
    trend = "Bullish" if tech["price"] > tech["MA50"] else "Bearish"

    # 🔹 Step 3: Structured output (NEW 🔥)
    data = {
        "symbol": symbol,
        "price": tech["price"],
        "indicators": {
            "MA20": tech["MA20"],
            "MA50": tech["MA50"],
            "RSI": tech["RSI"]
        },
        "trend": trend,
        "sentiment": sentiment
    }

    # 🔹 Step 4: AI / report layer
    report = generate_report(data)

    return {
        "data": data,
        "report": report
    }


def generate_report(data):
    return f"""
Financial Research Report

Stock: {data['symbol']}

Current Price: {data['price']}

Technical Indicators
MA20: {data['indicators']['MA20']}
MA50: {data['indicators']['MA50']}
RSI: {data['indicators']['RSI']}

Trend: {data['trend']}

News Sentiment: {data['sentiment']}

Conclusion:
This stock shows a {data['trend']} technical structure with {data['sentiment']} media sentiment.

Disclaimer: This is not investment advice.
"""

    return report