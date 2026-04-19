import sqlite3
import json
from datetime import datetime

DB_NAME = "financial.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Stock cache
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_cache (
            symbol TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    # Sentiment cache
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_cache (
            company TEXT PRIMARY KEY,
            sentiment TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    # Watchlist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            symbol TEXT PRIMARY KEY,
            added_at TEXT NOT NULL
        )
    """)

    # Portfolio
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            buy_price REAL NOT NULL,
            added_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# -------------------------
# STOCK CACHE
# -------------------------
def cache_stock(symbol, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO stock_cache (symbol, data, timestamp)
        VALUES (?, ?, ?)
    """, (
        symbol,
        json.dumps(data),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_cached_stock(symbol):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT data FROM stock_cache WHERE symbol = ?", (symbol,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return json.loads(row["data"])
    return None


# -------------------------
# SENTIMENT CACHE
# -------------------------
def cache_sentiment(company, sentiment):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO sentiment_cache (company, sentiment, timestamp)
        VALUES (?, ?, ?)
    """, (
        company,
        sentiment,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_cached_sentiment(company):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT sentiment FROM sentiment_cache WHERE company = ?", (company,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return row["sentiment"]
    return None


# -------------------------
# WATCHLIST
# -------------------------
def add_to_watchlist(symbol):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO watchlist (symbol, added_at)
        VALUES (?, ?)
    """, (
        symbol,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_watchlist():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT symbol, added_at FROM watchlist ORDER BY added_at DESC")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "symbol": row["symbol"],
            "added_at": row["added_at"]
        }
        for row in rows
    ]


def remove_from_watchlist(symbol):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM watchlist WHERE symbol = ?", (symbol,))
    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted > 0


# -------------------------
# PORTFOLIO
# -------------------------
def add_portfolio_stock(symbol, quantity, buy_price):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO portfolio (symbol, quantity, buy_price, added_at)
        VALUES (?, ?, ?, ?)
    """, (
        symbol,
        quantity,
        buy_price,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_portfolio_stocks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, symbol, quantity, buy_price, added_at
        FROM portfolio
        ORDER BY added_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row["id"],
            "symbol": row["symbol"],
            "quantity": row["quantity"],
            "buy_price": row["buy_price"],
            "added_at": row["added_at"]
        }
        for row in rows
    ]


def remove_portfolio_stock(stock_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM portfolio WHERE id = ?", (stock_id,))
    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted > 0