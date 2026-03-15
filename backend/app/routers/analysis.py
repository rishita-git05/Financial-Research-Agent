from fastapi import APIRouter
from app.agents.financial_agent import analyze_stock

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/{symbol}")
def stock_analysis(symbol: str):
    result = analyze_stock(symbol)
    return {"analysis": result}