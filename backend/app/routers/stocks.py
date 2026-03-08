from fastapi import APIRouter
from app.services.stock_service import get_stock_price

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"]
)

@router.get("/{symbol}")
def stock_price(symbol: str):
    return get_stock_price(symbol)