from fastapi import FastAPI
from app.routers import stocks, portfolio, analysis, watchlist, fundamentals, macro
from app.database import init_db

app = FastAPI(title="Financial Research AI Agent")

init_db()

app.include_router(stocks.router)
app.include_router(portfolio.router)
app.include_router(analysis.router)
app.include_router(watchlist.router)
app.include_router(fundamentals.router)
app.include_router(macro.router)

@app.get("/")
def home():
    return {"message": "Financial AI Agent API running"}