# 📊 Financial Research AI Agent

A full-stack financial analysis application that helps users analyze Indian stocks using technical indicators, fundamentals, sentiment analysis, and AI-driven insights.

---

## 🚀 Overview

The Financial Research AI Agent combines financial analytics with AI-based reasoning to generate structured investment recommendations such as **Buy, Hold, or Sell**.

It integrates:
- Technical analysis
- Fundamental analysis
- News sentiment
- AI-based scoring system
- Interactive dashboards
- Portfolio tracking

---

## 🎯 Features

### 📈 Stock Analysis
- Real-time stock data using Yahoo Finance
- Technical indicators:
  - RSI (Relative Strength Index)
  - MACD
  - Moving Averages (MA20, MA50)
  - Bollinger Bands
- Trend detection (Bullish / Bearish / Neutral)

---

### 🧠 AI-Based Decision System
- Multi-factor scoring system
- Generates:
  - Final score
  - Recommendation (BUY / HOLD / SELL)
- AI explanation for decisions
- Gemini AI integration (with fallback handling)

---

### 📰 Sentiment Analysis
- News-based sentiment classification
- Positive / Neutral / Negative detection
- Visual sentiment dashboard

---

### 📊 Visualizations
- Interactive price charts (Plotly)
- Moving averages overlay
- Portfolio analytics:
  - Pie chart (allocation)
  - Bar chart (profit/loss)

---

### 📂 Portfolio Management
- Add/remove stocks
- Track:
  - Investment value
  - Profit/Loss
  - Overall return %
- Portfolio recommendations

---

### ⭐ Watchlist
- Add/remove stocks
- Track selected stocks

---

### 📄 PDF Report
- Download full stock analysis reports
- Includes:
  - Technical analysis
  - Fundamentals
  - Signals
  - Final decision

---

### 🤖 Gemini AI Integration
- Generates professional insights
- Provides:
  - Analysis
  - Risk factors
  - Investment outlook
- Includes fallback when API limit is reached

---

## 🏗️ Tech Stack

### Backend
- FastAPI
- Python
- SQLite
- yfinance

### Frontend
- Streamlit
- Plotly
- Pandas

### AI
- Google Gemini API (`google-genai`)
- Rule-based fallback logic

---

## 📁 Project Structure
Financial-Research-Agent/
│
├── backend/
│   ├── app/
│   │   ├── agents/              # AI logic & decision system
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic (stocks, analysis, etc.)
│   │   ├── utils/               # Helper utilities
│   │   ├── database.py          # Database setup
│   │   └── main.py              # FastAPI entry point
│   │
│   └── requirements.txt
│
├── frontend/
│   └── streamlit_app.py         # Streamlit UI
│
├── .env                         # API keys (not committed)
├── .gitignore
└── README.md