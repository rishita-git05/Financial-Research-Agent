import re
from datetime import date
from fastapi import HTTPException, status

INDIAN_STOCK_PATTERN = r"^[A-Z0-9\-&]+(\.(NS|BO))?$"


def normalize_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()

    if not re.match(INDIAN_STOCK_PATTERN, symbol):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid stock symbol format. Use examples like TCS.NS, INFY.NS, RELIANCE.NS"
        )

    # default to NSE if no suffix
    if "." not in symbol:
        symbol = f"{symbol}.NS"

    return symbol


def validate_date_range(start_date: str | None = None, end_date: str | None = None):
    if not start_date or not end_date:
        return

    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )

    if start > end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date cannot be after end date"
        )


def validate_quantity(quantity: int):
    if quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0"
        )
    return quantity


def validate_buy_price(price: float):
    if price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Buy price must be greater than 0"
        )
    return price