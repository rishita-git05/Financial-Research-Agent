from fastapi import APIRouter, Query
from app.services.stock_service import get_stock_price, get_historical_data
from app.agents.financial_agent import analyze_stock
from app.utils.validators import normalize_symbol
import datetime

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"]
)


@router.get("/compare")
def compare_stocks(symbols: str = Query(..., description="Comma-separated stock symbols")):
    raw_symbols = [symbol.strip() for symbol in symbols.split(",") if symbol.strip()]

    if len(raw_symbols) < 2:
        return {"error": "Please provide at least two stock symbols for comparison"}

    symbol_list = [normalize_symbol(symbol) for symbol in raw_symbols]
    results = [analyze_stock(symbol) for symbol in symbol_list]

    return {"comparison": results}


@router.get("/market/status")
def market_status():
    now = datetime.datetime.now()
    weekday = now.weekday()

    open_time = now.replace(hour=9, minute=15, second=0, microsecond=0)
    close_time = now.replace(hour=15, minute=30, second=0, microsecond=0)

    if weekday >= 5:
        status = "CLOSED"
        message = "Market is closed today (weekend)"
    elif open_time <= now <= close_time:
        status = "OPEN"
        message = "Market is currently open"
    else:
        status = "CLOSED"
        message = "Market is currently closed"

    return {
        "market": "NSE",
        "status": status,
        "message": message,
        "time": now.strftime("%Y-%m-%d %H:%M:%S")
    }


@router.get("/{symbol}/history")
def stock_history(
    symbol: str,
    period: str = Query("1mo", description="Valid periods: 5d, 1mo, 3mo, 6mo, 1y")
):
    symbol = normalize_symbol(symbol)

    valid_periods = ["5d", "1mo", "3mo", "6mo", "1y"]
    if period not in valid_periods:
        return {
            "error": f"Invalid period '{period}'. Allowed values: {', '.join(valid_periods)}"
        }

    return get_historical_data(symbol, period)


@router.get("/{symbol}")
def stock_price(symbol: str):
    symbol = normalize_symbol(symbol)
    return get_stock_price(symbol)