from app.services.stock_service import get_stock_price
from app.agents.financial_agent import analyze_stock


portfolio = []

def add_stock(symbol, quantity, buy_price):
    portfolio.append({
        "symbol": symbol,
        "quantity": quantity,
        "buy_price": buy_price
    })
    return {"message": "Stock added"}

def get_portfolio():
    return portfolio


def get_portfolio_summary():
    summary = []
    total_invested = 0
    total_current = 0

    for stock in portfolio:
        current_price_data = get_stock_price(stock["symbol"])

        # handle dict or float
        if isinstance(current_price_data, dict):
            current_price = current_price_data.get("price", 0)
        else:
            current_price = current_price_data

        current_value = round(current_price * stock["quantity"], 2)
        invested_value = round(stock["buy_price"] * stock["quantity"], 2)
        profit_loss = round(current_value - invested_value, 2)

        total_invested += invested_value
        total_current += current_value

        summary.append({
            "symbol": stock["symbol"],
            "quantity": stock["quantity"],
            "buy_price": stock["buy_price"],
            "current_price": current_price,
            "current_value": current_value,
            "invested_value": invested_value,
            "profit_loss": profit_loss
        })

    return {
        "stocks": summary,
        "total_invested": round(total_invested, 2),
        "total_current": round(total_current, 2),
        "total_profit_loss": round(total_current - total_invested, 2)
    }

def get_recommendations():
    recommendations = []

    for stock in portfolio:
        try:
            analysis = analyze_stock(stock["symbol"])
            data = analysis["data"]
        except Exception as e:
            recommendations.append({
                "symbol": stock["symbol"],
                "decision": "ERROR",
                "reason": str(e)
            })
            continue

        rsi = data["indicators"].get("RSI", 50)
        trend = data["trend"]
        sentiment = data["sentiment"]

        # 🔥 Improved decision logic
        if trend == "Bullish" and rsi < 60:
            decision = "BUY"
        elif trend == "Bearish" and rsi > 40:
            decision = "SELL"
        elif rsi < 30:
            decision = "STRONG BUY"
        elif rsi > 70:
            decision = "STRONG SELL"
        else:
            decision = "HOLD"

        reason = f"Trend: {trend}, RSI: {rsi:.2f}, Sentiment: {sentiment}"

        if rsi < 30:
            reason += " (Oversold)"
        elif rsi > 70:
            reason += " (Overbought)"

        recommendations.append({
            "symbol": stock["symbol"],
            "decision": decision,
            "reason": reason
        })

    return recommendations