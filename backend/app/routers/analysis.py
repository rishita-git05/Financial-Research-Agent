from fastapi import APIRouter
from app.agents.financial_agent import analyze_stock
from app.utils.validators import normalize_symbol

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


@router.get("/{symbol}")
def stock_analysis(symbol: str):
    symbol = normalize_symbol(symbol)
    return analyze_stock(symbol)