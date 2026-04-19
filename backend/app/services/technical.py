import yfinance as yf
from fastapi import HTTPException, status


def get_technical_indicators(symbol: str):
    symbol = symbol.upper().strip()

    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="6mo")

        if df.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No technical data found for {symbol}"
            )

        df["MA20"] = df["Close"].rolling(window=20).mean()
        df["MA50"] = df["Close"].rolling(window=50).mean()

        delta = df["Close"].diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

        rs = gain / (loss + 1e-10)
        df["RSI"] = 100 - (100 / (1 + rs))

        latest = df.iloc[-1]

        return {
            "symbol": symbol,
            "price": round(float(latest["Close"]), 2),
            "MA20": round(float(latest["MA20"]), 2) if not df["MA20"].isna().iloc[-1] else None,
            "MA50": round(float(latest["MA50"]), 2) if not df["MA50"].isna().iloc[-1] else None,
            "RSI": round(float(latest["RSI"]), 2) if not df["RSI"].isna().iloc[-1] else None
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate technical indicators for {symbol}: {str(e)}"
        )