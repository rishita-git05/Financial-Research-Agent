import yfinance as yf
from fastapi import HTTPException, status


def moving_average(symbol: str):
    symbol = symbol.upper().strip()

    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="3mo")

        if hist.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No moving average data found for {symbol}"
            )

        hist["MA20"] = hist["Close"].rolling(window=20).mean()

        data = hist.tail(5)[["Close", "MA20"]].reset_index()

        if "Date" in data.columns:
            data["Date"] = data["Date"].astype(str)

        records = []
        for _, row in data.iterrows():
            records.append({
                "Date": row["Date"] if "Date" in row else None,
                "Close": round(float(row["Close"]), 2) if row["Close"] is not None else None,
                "MA20": round(float(row["MA20"]), 2) if row["MA20"] == row["MA20"] else None
            })

        return records

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate moving average for {symbol}: {str(e)}"
        )