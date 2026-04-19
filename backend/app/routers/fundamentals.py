from fastapi import APIRouter
from app.services.fundamental_service import get_fundamentals
from app.utils.validators import normalize_symbol

router = APIRouter(
    prefix="/fundamentals",
    tags=["Fundamentals"]
)

@router.get("/{symbol}")
def fundamentals(symbol: str):
    symbol = normalize_symbol(symbol)
    return get_fundamentals(symbol)