from fastapi import HTTPException, status
from app.database import (
    add_portfolio_stock,
    get_portfolio_stocks,
    remove_portfolio_stock
)
from app.services.stock_service import get_stock_price
from app.agents.financial_agent import analyze_stock
from app.utils.validators import normalize_symbol, validate_quantity, validate_buy_price


def add_stock(symbol, quantity, buy_price):
    symbol = normalize_symbol(symbol)
    quantity = validate_quantity(quantity)
    buy_price = validate_buy_price(buy_price)

    add_portfolio_stock(symbol, quantity, buy_price)

    return {
        "message": "Stock added to portfolio",
        "symbol": symbol,
        "quantity": quantity,
        "buy_price": buy_price
    }


def get_portfolio():
    return get_portfolio_stocks()


def delete_stock(stock_id: int):
    deleted = remove_portfolio_stock(stock_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No portfolio stock found with id {stock_id}"
        )

    return {"message": f"Portfolio stock with id {stock_id} removed successfully"}


def get_portfolio_summary():
    portfolio = get_portfolio_stocks()

    summary = []
    total_invested = 0
    total_current = 0

    for stock in portfolio:
        current_price_data = get_stock_price(stock["symbol"])
        current_price = current_price_data.get("price", 0)

        current_value = round(current_price * stock["quantity"], 2)
        invested_value = round(stock["buy_price"] * stock["quantity"], 2)
        profit_loss = round(current_value - invested_value, 2)

        total_invested += invested_value
        total_current += current_value

        summary.append({
            "id": stock["id"],
            "symbol": stock["symbol"],
            "quantity": stock["quantity"],
            "buy_price": stock["buy_price"],
            "current_price": current_price,
            "current_value": current_value,
            "invested_value": invested_value,
            "profit_loss": profit_loss
        })

    overall_return_percent = round(
        ((total_current - total_invested) / total_invested) * 100, 2
    ) if total_invested > 0 else 0

    # Add allocation %
    for stock in summary:
        stock["allocation_percent"] = round(
            (stock["current_value"] / total_current) * 100, 2
        ) if total_current > 0 else 0

    best_performer = None
    worst_performer = None

    if summary:
        best_performer = max(summary, key=lambda x: x["profit_loss"])
        worst_performer = min(summary, key=lambda x: x["profit_loss"])

    diversification = get_diversification_insight(summary)

    return {
        "stocks": summary,
        "total_invested": round(total_invested, 2),
        "total_current": round(total_current, 2),
        "total_profit_loss": round(total_current - total_invested, 2),
        "overall_return_percent": overall_return_percent,
        "best_performer": {
            "symbol": best_performer["symbol"],
            "profit_loss": best_performer["profit_loss"]
        } if best_performer else None,
        "worst_performer": {
            "symbol": worst_performer["symbol"],
            "profit_loss": worst_performer["profit_loss"]
        } if worst_performer else None,
        "diversification_insight": diversification
    }


def get_diversification_insight(summary):
    if not summary:
        return "No portfolio data available"

    if len(summary) == 1:
        return "Highly concentrated portfolio"

    max_allocation = max(stock["allocation_percent"] for stock in summary)

    if max_allocation > 60:
        return "Portfolio is concentrated in one major holding"
    elif max_allocation > 40:
        return "Portfolio has moderate concentration risk"
    return "Portfolio appears reasonably diversified"


def get_recommendations():
    portfolio = get_portfolio_stocks()
    recommendations = []

    for stock in portfolio:
        analysis = analyze_stock(stock["symbol"])
        data = analysis["data"]

        rsi = data["indicators"].get("RSI")
        trend = data.get("trend", "Neutral")
        sentiment = data.get("sentiment", "Neutral")
        rsi_signal = data.get("rsi_signal", "Neutral")
        macd_signal_text = data.get("macd_signal_text", "Neutral")
        bollinger_signal = data.get("bollinger_signal", "Neutral")

        if rsi is None:
            decision = "HOLD"
            reason = f"Trend: {trend}, RSI unavailable, Sentiment: {sentiment}"
        elif trend in ["Strong Bullish", "Bullish"] and rsi < 60 and sentiment != "Negative":
            decision = "BUY"
            reason = (
                f"Trend: {trend}, RSI: {rsi:.2f}, Sentiment: {sentiment}, "
                f"MACD: {macd_signal_text}, Bands: {bollinger_signal}"
            )
        elif trend in ["Strong Bearish", "Bearish"] and rsi > 40:
            decision = "SELL"
            reason = (
                f"Trend: {trend}, RSI: {rsi:.2f}, Sentiment: {sentiment}, "
                f"MACD: {macd_signal_text}, Bands: {bollinger_signal}"
            )
        elif rsi < 30:
            decision = "STRONG BUY"
            reason = (
                f"RSI: {rsi:.2f} ({rsi_signal}), Trend: {trend}, "
                f"MACD: {macd_signal_text}, Bands: {bollinger_signal}"
            )
        elif rsi > 70:
            decision = "STRONG SELL"
            reason = (
                f"RSI: {rsi:.2f} ({rsi_signal}), Trend: {trend}, "
                f"MACD: {macd_signal_text}, Bands: {bollinger_signal}"
            )
        else:
            decision = "HOLD"
            reason = (
                f"Trend: {trend}, RSI: {rsi:.2f}, Sentiment: {sentiment}, "
                f"MACD: {macd_signal_text}, Bands: {bollinger_signal}"
            )

        recommendations.append({
            "id": stock["id"],
            "symbol": stock["symbol"],
            "decision": decision,
            "reason": reason
        })

    return recommendations