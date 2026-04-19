from app.services.technical import get_technical_indicators
from app.services.news import get_news_sentiment
from app.services.fundamental_service import get_fundamentals


def analyze_stock(symbol: str):
    symbol = symbol.upper().strip()

    tech = get_technical_indicators(symbol)
    fundamentals = get_fundamentals(symbol)
    company_name = symbol.split(".")[0]
    sentiment = get_news_sentiment(company_name)

    price = tech.get("price")
    ma20 = tech.get("MA20")
    ma50 = tech.get("MA50")
    rsi = tech.get("RSI")

    trend = interpret_trend(price, ma20, ma50)
    rsi_signal = interpret_rsi(rsi)
    valuation_signal = interpret_valuation(fundamentals.get("pe_ratio"))
    debt_signal = interpret_debt(fundamentals.get("debt_to_equity"))
    growth_signal = interpret_growth(
        fundamentals.get("revenue_growth"),
        fundamentals.get("earnings_growth")
    )

    data = {
        "symbol": symbol,
        "price": price,
        "indicators": {
            "MA20": ma20,
            "MA50": ma50,
            "RSI": rsi
        },
        "trend": trend,
        "rsi_signal": rsi_signal,
        "sentiment": sentiment,
        "fundamentals": {
            "name": fundamentals.get("name"),
            "sector": fundamentals.get("sector"),
            "industry": fundamentals.get("industry"),
            "market_cap": fundamentals.get("market_cap"),
            "pe_ratio": fundamentals.get("pe_ratio"),
            "forward_pe": fundamentals.get("forward_pe"),
            "dividend_yield": fundamentals.get("dividend_yield"),
            "debt_to_equity": fundamentals.get("debt_to_equity"),
            "revenue_growth": fundamentals.get("revenue_growth"),
            "earnings_growth": fundamentals.get("earnings_growth"),
            "return_on_equity": fundamentals.get("return_on_equity"),
            "currency": fundamentals.get("currency")
        },
        "signals": {
            "valuation": valuation_signal,
            "debt": debt_signal,
            "growth": growth_signal
        }
    }

    report = generate_report(data)

    return {
        "data": data,
        "report": report
    }


def interpret_trend(price, ma20, ma50):
    if price is None or ma20 is None or ma50 is None:
        return "Insufficient Data"

    if price > ma20 and ma20 > ma50:
        return "Strong Bullish"
    elif price > ma50:
        return "Bullish"
    elif price < ma20 and ma20 < ma50:
        return "Strong Bearish"
    elif price < ma50:
        return "Bearish"
    return "Neutral"


def interpret_rsi(rsi):
    if rsi is None:
        return "Insufficient Data"

    if rsi > 70:
        return "Overbought"
    elif rsi < 30:
        return "Oversold"
    return "Neutral"


def interpret_valuation(pe_ratio):
    if pe_ratio in [None, "N/A"]:
        return "Insufficient Data"

    try:
        pe_ratio = float(pe_ratio)
    except Exception:
        return "Insufficient Data"

    if pe_ratio < 15:
        return "Potentially Undervalued"
    elif pe_ratio > 30:
        return "Potentially Overvalued"
    return "Fairly Valued"


def interpret_debt(debt_to_equity):
    if debt_to_equity in [None, "N/A"]:
        return "Insufficient Data"

    try:
        debt_to_equity = float(debt_to_equity)
    except Exception:
        return "Insufficient Data"

    if debt_to_equity < 50:
        return "Low Debt"
    elif debt_to_equity > 150:
        return "High Debt"
    return "Moderate Debt"


def interpret_growth(revenue_growth, earnings_growth):
    if revenue_growth in [None, "N/A"] and earnings_growth in [None, "N/A"]:
        return "Insufficient Data"

    try:
        rev = float(revenue_growth) if revenue_growth not in [None, "N/A"] else 0
        earn = float(earnings_growth) if earnings_growth not in [None, "N/A"] else 0
    except Exception:
        return "Insufficient Data"

    if rev > 0 and earn > 0:
        return "Positive Growth"
    elif rev < 0 and earn < 0:
        return "Negative Growth"
    return "Mixed Growth"


def generate_report(data):
    f = data["fundamentals"]
    s = data["signals"]

    return f"""
Financial Research Report

Stock: {data['symbol']}
Company: {f['name']}
Sector: {f['sector']}
Industry: {f['industry']}
Currency: {f['currency']}

Current Price: {data['price']}

Technical Indicators
MA20: {data['indicators']['MA20']}
MA50: {data['indicators']['MA50']}
RSI: {data['indicators']['RSI']}

Technical View
Trend: {data['trend']}
RSI Signal: {data['rsi_signal']}

News Sentiment
Sentiment: {data['sentiment']}

Fundamental Overview
Market Cap: {f['market_cap']}
P/E Ratio: {f['pe_ratio']}
Forward P/E: {f['forward_pe']}
Dividend Yield: {f['dividend_yield']}
Debt to Equity: {f['debt_to_equity']}
Revenue Growth: {f['revenue_growth']}
Earnings Growth: {f['earnings_growth']}
Return on Equity: {f['return_on_equity']}

Fundamental Signals
Valuation: {s['valuation']}
Debt Profile: {s['debt']}
Growth Profile: {s['growth']}

Conclusion:
This stock currently shows a {data['trend']} technical structure with {data['sentiment']} news sentiment.
From a fundamental perspective, the stock appears {s['valuation']} with a {s['debt']} balance-sheet profile and {s['growth']}.

Disclaimer: This is not investment advice.
"""