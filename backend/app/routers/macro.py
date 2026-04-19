from fastapi import APIRouter
from app.services.macro_service import get_macro_dashboard, compare_with_nifty
from app.utils.validators import normalize_symbol

router = APIRouter(
    prefix="/macro",
    tags=["Macro & Market Context"]
)


@router.get("/")
def macro_dashboard():
    return get_macro_dashboard()


@router.get("/compare/{symbol}")
def market_comparison(symbol: str):
    symbol = normalize_symbol(symbol)
    return compare_with_nifty(symbol)