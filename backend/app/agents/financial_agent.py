from app.services.technical import get_technical_indicators
from app.services.news import get_news_sentiment
from app.services.fundamental_service import get_fundamentals
from app.services.ai_agent import generate_ai_analysis


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


def interpret_macd(macd, macd_signal):
    if macd is None or macd_signal is None:
        return "Insufficient Data"

    if macd > macd_signal:
        return "Bullish MACD Crossover"
    elif macd < macd_signal:
        return "Bearish MACD Crossover"
    return "Neutral"


def interpret_bollinger(price, upper, lower):
    if price is None or upper is None or lower is None:
        return "Insufficient Data"

    if price > upper:
        return "Above Upper Band"
    elif price < lower:
        return "Below Lower Band"
    return "Within Bands"


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


def generate_final_decision(data):
    score = 0

    trend = data.get("trend", "")
    rsi = data.get("indicators", {}).get("RSI", 50)
    sentiment = data.get("sentiment", "Neutral")
    valuation = data.get("signals", {}).get("valuation", "")
    growth = data.get("signals", {}).get("growth", "")
    debt = data.get("signals", {}).get("debt", "")

    # Trend scoring
    if trend == "Strong Bullish":
        score += 2
    elif trend == "Bullish":
        score += 1
    elif trend == "Strong Bearish":
        score -= 2
    elif trend == "Bearish":
        score -= 1

    # RSI scoring
    if isinstance(rsi, (int, float)):
        if rsi < 30:
            score += 2
        elif rsi > 70:
            score -= 2

    # Sentiment scoring
    if sentiment == "Positive":
        score += 1
    elif sentiment == "Negative":
        score -= 1

    # Valuation scoring
    if valuation == "Potentially Undervalued":
        score += 1
    elif valuation == "Potentially Overvalued":
        score -= 1

    # Growth scoring
    if growth == "Positive Growth":
        score += 1
    elif growth == "Negative Growth":
        score -= 1

    # Debt scoring
    if debt == "Low Debt":
        score += 1
    elif debt == "High Debt":
        score -= 1

    return score


def generate_decision_label(score):
    if score >= 5:
        return "STRONG BUY"
    elif score >= 3:
        return "BUY"
    elif score >= 1:
        return "WEAK BUY"
    elif score == 0:
        return "HOLD"
    elif score <= -5:
        return "STRONG SELL"
    elif score <= -3:
        return "SELL"
    return "WEAK SELL"

def generate_ai_explanation(data):
    trend = data.get("trend")
    rsi = data.get("indicators", {}).get("RSI")
    sentiment = data.get("sentiment")
    valuation = data.get("signals", {}).get("valuation")
    growth = data.get("signals", {}).get("growth")
    debt = data.get("signals", {}).get("debt")

    explanation = []

    # Trend
    if "Bullish" in trend:
        explanation.append("The stock is showing a bullish trend.")
    elif "Bearish" in trend:
        explanation.append("The stock is currently in a bearish trend.")

    # RSI
    if isinstance(rsi, (int, float)):
        if rsi < 30:
            explanation.append("RSI indicates the stock may be oversold.")
        elif rsi > 70:
            explanation.append("RSI indicates the stock may be overbought.")

    # Sentiment
    if sentiment == "Positive":
        explanation.append("News sentiment is positive, supporting upward movement.")
    elif sentiment == "Negative":
        explanation.append("News sentiment is negative, indicating caution.")

    # Fundamentals
    explanation.append(f"Valuation appears {valuation}.")
    explanation.append(f"Growth profile is {growth}.")
    explanation.append(f"Debt profile is {debt}.")

    return " ".join(explanation)


def generate_report(data):
    f = data["fundamentals"]
    s = data["signals"]
    i = data["indicators"]

    return f"""
Financial Research Report

Stock: {data['symbol']}
Company: {f['name']}
Sector: {f['sector']}
Industry: {f['industry']}
Currency: {f['currency']}

Current Price: {data['price']}

Technical Indicators
MA20: {i['MA20']}
MA50: {i['MA50']}
RSI: {i['RSI']}
MACD: {i['MACD']}
MACD Signal: {i['MACD_SIGNAL']}
Bollinger Upper: {i['BB_UPPER']}
Bollinger Middle: {i['BB_MIDDLE']}
Bollinger Lower: {i['BB_LOWER']}

Technical View
Trend: {data['trend']}
RSI Signal: {data['rsi_signal']}
MACD Interpretation: {data['macd_signal_text']}
Bollinger Interpretation: {data['bollinger_signal']}

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

Final AI Decision
Score: {data['final_score']}
Recommendation: {data['final_decision']}

AI Explanation:
{data.get("ai_explanation")}

Conclusion:
This stock currently shows a {data['trend']} technical structure with {data['sentiment']} news sentiment.
Additional technical signals suggest {data['macd_signal_text']} and price action is {data['bollinger_signal']}.
From a fundamental perspective, the stock appears {s['valuation']} with a {s['debt']} balance-sheet profile and {s['growth']}.
Overall, the AI-based recommendation for this stock is {data['final_decision']}.

Disclaimer: This is not investment advice.
"""


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
    macd = tech.get("MACD")
    macd_signal = tech.get("MACD_SIGNAL")
    bb_upper = tech.get("BB_UPPER")
    bb_middle = tech.get("BB_MIDDLE")
    bb_lower = tech.get("BB_LOWER")

    trend = interpret_trend(price, ma20, ma50)
    rsi_signal = interpret_rsi(rsi)
    macd_signal_text = interpret_macd(macd, macd_signal)
    bollinger_signal = interpret_bollinger(price, bb_upper, bb_lower)

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
            "RSI": rsi,
            "MACD": macd,
            "MACD_SIGNAL": macd_signal,
            "BB_UPPER": bb_upper,
            "BB_MIDDLE": bb_middle,
            "BB_LOWER": bb_lower
        },
        "trend": trend,
        "rsi_signal": rsi_signal,
        "macd_signal_text": macd_signal_text,
        "bollinger_signal": bollinger_signal,
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

    final_score = generate_final_decision(data)
    final_decision = generate_decision_label(final_score)

    data["final_score"] = final_score
    data["final_decision"] = final_decision

    ai_explanation = generate_ai_explanation(data)
    data["ai_explanation"] = ai_explanation

    report = generate_report(data)

    ai_analysis = generate_ai_analysis(data)

    data["llm_analysis"] = ai_analysis
    

    return {
        "data": data,
        "report": report,
        "llm_analysis": ai_analysis
    }