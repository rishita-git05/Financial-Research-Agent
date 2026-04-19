import os
import requests
from textblob import TextBlob
from app.database import cache_sentiment, get_cached_sentiment

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def get_news_sentiment(company: str):
    company = company.strip()

    # 1. Check cache first
    cached = get_cached_sentiment(company)
    if cached:
        return cached

    # 2. If API key missing, fail safely
    if not NEWS_API_KEY:
        return "Neutral"

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={company}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return "Neutral"

        articles = response.json().get("articles", [])[:5]

        sentiments = []

        for article in articles:
            title = article.get("title", "").strip()
            if title:
                polarity = TextBlob(title).sentiment.polarity
                sentiments.append(polarity)

        if not sentiments:
            sentiment = "Neutral"
        else:
            avg = sum(sentiments) / len(sentiments)

            if avg > 0.2:
                sentiment = "Positive"
            elif avg < -0.2:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

        # 3. Cache result
        cache_sentiment(company, sentiment)

        return sentiment

    except Exception:
        return "Neutral"