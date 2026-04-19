import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_ai_analysis(data):
    try:
        prompt = f"""
You are a financial analyst AI.

Analyze the following stock data and give a professional investment insight.

Stock: {data['symbol']}
Price: {data['price']}
Trend: {data['trend']}
RSI: {data['indicators']['RSI']}
MACD Signal: {data['macd_signal_text']}
Bollinger Signal: {data['bollinger_signal']}

Sentiment: {data['sentiment']}

Fundamentals:
- Market Cap: {data['fundamentals']['market_cap']}
- P/E Ratio: {data['fundamentals']['pe_ratio']}
- Revenue Growth: {data['fundamentals']['revenue_growth']}
- Earnings Growth: {data['fundamentals']['earnings_growth']}
- Debt to Equity: {data['fundamentals']['debt_to_equity']}

Signals:
- Valuation: {data['signals']['valuation']}
- Growth: {data['signals']['growth']}
- Debt: {data['signals']['debt']}

Final Score: {data['final_score']}
Recommendation: {data['final_decision']}

Give:
1. Short professional analysis
2. Risk factors
3. Investment outlook (short-term and long-term)

Keep it concise and clear.
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        if response and hasattr(response, "candidates"):
            try:
                return response.candidates[0].content.parts[0].text.strip()
            except Exception:
                pass

        return "AI analysis generated but could not be parsed."

    except Exception as e:
        error_str = str(e)

        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            return "AI insights currently unavailable due to API limits. Showing rule-based analysis instead."

        return "AI insights could not be generated at this time."