from fastapi import APIRouter
from app.services.stock_service import get_stock_price
from app.services.stock_service import get_historical_data
import datetime

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"]
)

@router.get("/{symbol}")
def stock_price(symbol: str):
    return get_stock_price(symbol)

@router.get("/{symbol}/history")
def stock_history(symbol: str):
    return get_historical_data(symbol)

@router.get("/market/status")
def market_status():
    now = datetime.datetime.now()

    open_time = now.replace(hour=9, minute=15)
    close_time = now.replace(hour=15, minute=30)

    if open_time <= now <= close_time:
        status = "OPEN"
    else:
        status = "CLOSED"

    return {"market": "NSE", "status": status}