import yfinance as yf
from fastapi import HTTPException, status
from app.database import cache_stock, get_cached_stock


def get_stock_price(symbol: str):
    symbol = symbol.upper().strip()

    cached = get_cached_stock(symbol)
    if cached:
        return cached

    try:
        stock = yf.Ticker(symbol)
        info = stock.info or {}

        price = info.get("currentPrice")

        if price is None:
            hist = stock.history(period="1d")
            if hist.empty:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No price data found for {symbol}"
                )
            price = float(hist["Close"].iloc[-1])

        data = {
            "symbol": symbol,
            "name": info.get("longName", symbol),
            "price": float(price),
            "market_cap": info.get("marketCap", "N/A"),
            "currency": info.get("currency", "INR"),
            "source": "yfinance"
        }

        cache_stock(symbol, data)
        return data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch stock price for {symbol}: {str(e)}"
        )


def get_historical_data(symbol: str, period: str = "1mo"):
    symbol = symbol.upper().strip()

    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)

        if hist.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No historical data found for {symbol}"
            )

        hist = hist.reset_index()

        if "Date" in hist.columns:
            hist["Date"] = hist["Date"].astype(str)

        return hist.to_dict(orient="records")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch historical data for {symbol}: {str(e)}"
        )