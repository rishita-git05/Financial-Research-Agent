from fastapi import APIRouter
from app.services.portfolio import add_stock, get_portfolio, get_portfolio_summary, get_recommendations


router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)

@router.post("/add")
def add(symbol: str, quantity: int, buy_price: float):
    return add_stock(symbol.upper(), quantity, buy_price)

@router.get("/")
def view():
    return get_portfolio()

@router.get("/summary")
def summary():
    return get_portfolio_summary()

@router.get("/recommendations")
def recommendations():
    return get_recommendations()