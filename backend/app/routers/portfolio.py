from fastapi import APIRouter
from app.services.portfolio import (
    add_stock,
    get_portfolio,
    get_portfolio_summary,
    get_recommendations,
    delete_stock
)

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


@router.delete("/{stock_id}")
def remove(stock_id: int):
    return delete_stock(stock_id)