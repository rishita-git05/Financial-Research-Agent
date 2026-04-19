import yfinance as yf
from fastapi import HTTPException, status


MACRO_SYMBOLS = {
    "NIFTY_50": "^NSEI",
    "SENSEX": "^BSESN",
    "USD_INR": "INR=X",
    "GOLD": "GC=F",
    "CRUDE_OIL": "CL=F"
}


def fetch_macro_quote(name: str, symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d")

        if hist.empty:
            return {
                "name": name,
                "symbol": symbol,
                "error": "No data available"
            }

        latest_close = float(hist["Close"].iloc[-1])
        previous_close = float(hist["Close"].iloc[-2]) if len(hist) > 1 else latest_close
        change = round(latest_close - previous_close, 2)
        pct_change = round((change / previous_close) * 100, 2) if previous_close != 0 else 0

        return {
            "name": name,
            "symbol": symbol,
            "latest_close": round(latest_close, 2),
            "change": change,
            "percent_change": pct_change
        }

    except Exception as e:
        return {
            "name": name,
            "symbol": symbol,
            "error": str(e)
        }


def get_macro_dashboard():
    return {
        "macro_indicators": [
            fetch_macro_quote(name, symbol)
            for name, symbol in MACRO_SYMBOLS.items()
        ]
    }


def compare_with_nifty(stock_symbol: str):
    try:
        stock = yf.Ticker(stock_symbol)
        stock_hist = stock.history(period="1mo")

        nifty = yf.Ticker("^NSEI")
        nifty_hist = nifty.history(period="1mo")

        if stock_hist.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No historical data found for {stock_symbol}"
            )

        if nifty_hist.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No NIFTY data found"
            )

        stock_return = (
            (float(stock_hist["Close"].iloc[-1]) - float(stock_hist["Close"].iloc[0]))
            / float(stock_hist["Close"].iloc[0])
        ) * 100

        nifty_return = (
            (float(nifty_hist["Close"].iloc[-1]) - float(nifty_hist["Close"].iloc[0]))
            / float(nifty_hist["Close"].iloc[0])
        ) * 100

        relative = round(stock_return - nifty_return, 2)

        if relative > 0:
            verdict = "Outperforming NIFTY 50"
        elif relative < 0:
            verdict = "Underperforming NIFTY 50"
        else:
            verdict = "In line with NIFTY 50"

        return {
            "stock_symbol": stock_symbol,
            "stock_return_percent_1m": round(stock_return, 2),
            "nifty_return_percent_1m": round(nifty_return, 2),
            "relative_performance_percent": relative,
            "verdict": verdict
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compare {stock_symbol} with NIFTY: {str(e)}"
        )