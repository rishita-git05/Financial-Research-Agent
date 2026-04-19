from fastapi import APIRouter, HTTPException
from app.database import add_to_watchlist, get_watchlist, remove_from_watchlist
from app.utils.validators import normalize_symbol

router = APIRouter(
    prefix="/watchlist",
    tags=["Watchlist"]
)


@router.post("/{symbol}")
def add_watchlist(symbol: str):
    symbol = normalize_symbol(symbol)
    add_to_watchlist(symbol)
    return {"message": f"{symbol} added to watchlist"}


@router.get("/")
def view_watchlist():
    return {"watchlist": get_watchlist()}


@router.delete("/{symbol}")
def delete_watchlist(symbol: str):
    symbol = normalize_symbol(symbol)
    deleted = remove_from_watchlist(symbol)

    if not deleted:
        raise HTTPException(status_code=404, detail=f"{symbol} not found in watchlist")

    return {"message": f"{symbol} removed from watchlist"}