import requests
from textblob import TextBlob
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news_sentiment(company):
    
    url = f"https://newsapi.org/v2/everything?q={company}&language=en&apiKey={NEWS_API_KEY}"

    response = requests.get(url)
    articles = response.json().get("articles", [])[:5]

    sentiments = []

    for article in articles:
        title = article["title"]
        polarity = TextBlob(title).sentiment.polarity
        sentiments.append(polarity)

    if not sentiments:
        return "Neutral"

    avg = sum(sentiments) / len(sentiments)

    if avg > 0.2:
        return "Positive"
    elif avg < -0.2:
        return "Negative"
    else:
        return "Neutral"