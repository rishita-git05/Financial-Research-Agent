from fastapi import APIRouter
from app.services.stock_service import get_stock_price, get_historical_data
from app.agents.financial_agent import analyze_stock
import datetime

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"]
)

# 🔥 1. Stock Comparison (PUT THIS FIRST to avoid conflicts)
@router.get("/compare")
def compare_stocks(symbols: str):
    symbol_list = symbols.split(",")

    results = []
    for symbol in symbol_list:
        results.append(analyze_stock(symbol.strip().upper()))

    return {
        "comparison": results
    }


# 🔹 2. Market Status
@router.get("/market/status")
def market_status():
    now = datetime.datetime.now()

    open_time = now.replace(hour=9, minute=15, second=0)
    close_time = now.replace(hour=15, minute=30, second=0)

    if open_time <= now <= close_time:
        status = "OPEN"
    else:
        status = "CLOSED"

    return {
        "market": "NSE",
        "status": status,
        "time": now.strftime("%Y-%m-%d %H:%M:%S")
    }


# 🔹 3. Historical Data
@router.get("/{symbol}/history")
def stock_history(symbol: str):
    return get_historical_data(symbol.upper())


# 🔹 4. Current Price (KEEP THIS LAST)
@router.get("/{symbol}")
def stock_price(symbol: str):
    return get_stock_price(symbol.upper())