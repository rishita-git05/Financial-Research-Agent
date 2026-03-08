import yfinance as yf

def get_stock_price(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        if not info:
            return {"error": "Invalid stock symbol"}

        return {
            "symbol": symbol,
            "name": info.get("longName"),
            "price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
            "currency": info.get("currency")
        }

    except Exception as e:
        return {"error": str(e)}