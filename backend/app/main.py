from fastapi import FastAPI
from app.routers import stocks

from app.routers import stocks
from app.routers import analysis

app = FastAPI(title="Financial Research AI Agent")

app.include_router(stocks.router)

app.include_router(stocks.router)
app.include_router(analysis.router)

@app.get("/")
def home():
    return {"message": "Financial AI Agent API running"}
