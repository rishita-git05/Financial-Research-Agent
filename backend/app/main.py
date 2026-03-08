from fastapi import FastAPI
from app.routers import stocks

app = FastAPI(title="Financial Research AI Agent")

app.include_router(stocks.router)

@app.get("/")
def home():
    return {"message": "Financial AI Agent API running"}