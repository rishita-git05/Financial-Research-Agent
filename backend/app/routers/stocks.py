from fastapi import APIRouter
from app.services.stock_service import get_stock_price
from app.services.stock_service import get_historical_data

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