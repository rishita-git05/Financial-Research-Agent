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

        close = df["Close"]

        # Moving averages
        df["MA20"] = close.rolling(window=20).mean()
        df["MA50"] = close.rolling(window=50).mean()

        # RSI
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-10)
        df["RSI"] = 100 - (100 / (1 + rs))

        # MACD
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        df["MACD"] = ema12 - ema26
        df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()

        # Bollinger Bands
        rolling_std = close.rolling(window=20).std()
        df["BB_MIDDLE"] = df["MA20"]
        df["BB_UPPER"] = df["MA20"] + (2 * rolling_std)
        df["BB_LOWER"] = df["MA20"] - (2 * rolling_std)

        latest = df.iloc[-1]

        return {
            "symbol": symbol,
            "price": round(float(latest["Close"]), 2),
            "MA20": round(float(latest["MA20"]), 2) if not df["MA20"].isna().iloc[-1] else None,
            "MA50": round(float(latest["MA50"]), 2) if not df["MA50"].isna().iloc[-1] else None,
            "RSI": round(float(latest["RSI"]), 2) if not df["RSI"].isna().iloc[-1] else None,
            "MACD": round(float(latest["MACD"]), 4) if not df["MACD"].isna().iloc[-1] else None,
            "MACD_SIGNAL": round(float(latest["MACD_SIGNAL"]), 4) if not df["MACD_SIGNAL"].isna().iloc[-1] else None,
            "BB_UPPER": round(float(latest["BB_UPPER"]), 2) if not df["BB_UPPER"].isna().iloc[-1] else None,
            "BB_MIDDLE": round(float(latest["BB_MIDDLE"]), 2) if not df["BB_MIDDLE"].isna().iloc[-1] else None,
            "BB_LOWER": round(float(latest["BB_LOWER"]), 2) if not df["BB_LOWER"].isna().iloc[-1] else None
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate technical indicators for {symbol}: {str(e)}"
        )