# 📊 Financial Research AI Agent

A full-stack financial analysis platform that helps users analyze Indian stocks using technical indicators, fundamentals, sentiment analysis, and AI-powered insights.

---

## 🚀 Overview

The **Financial Research AI Agent** combines financial analytics with AI-based reasoning to generate structured stock recommendations such as:

- ✅ BUY  
- ⚖️ HOLD  
- ❌ SELL  

It integrates multiple systems into one intelligent dashboard:

- Technical Analysis  
- Fundamental Analysis  
- News Sentiment  
- AI-Based Scoring  
- Interactive Visualizations  
- Portfolio Tracking  

---

## 🎯 Features

### 📈 Stock Analysis

- Real-time stock data using **Yahoo Finance**
- Technical indicators:
  - RSI (Relative Strength Index)
  - MACD
  - Moving Averages (MA20, MA50)
  - Bollinger Bands
- Trend Detection:
  - Bullish
  - Bearish
  - Neutral

---

### 🧠 AI-Based Decision System

- Multi-factor scoring engine
- Generates:
  - Final Score
  - Recommendation (BUY / HOLD / SELL)
- AI-generated explanations
- Gemini AI integration with fallback handling

---

### 📰 Sentiment Analysis

- News-based sentiment classification
- Positive / Neutral / Negative detection
- Visual sentiment dashboard

---

### 📊 Interactive Visualizations

- Live price charts using **Plotly**
- Moving average overlays
- Portfolio analytics:
  - Allocation pie chart
  - Profit/Loss chart
  - Performance tracking

---

### 📂 Portfolio Management

- Add / Remove stocks
- Track:
  - Investment Value
  - Profit / Loss
  - Overall Return %
- Portfolio suggestions

---

### ⭐ Watchlist

- Add / Remove favorite stocks
- Track selected companies quickly

---

### 📄 PDF Report Generation

Generate downloadable reports including:

- Technical indicators
- Fundamentals
- Trading signals
- Final recommendation
- AI insights

---

### 🤖 Gemini AI Integration

Uses **Google Gemini API** for:

- Professional market insights
- Risk analysis
- Investment outlook
- Smart summaries

Includes fallback logic when API quota is reached.

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
- Rule-based fallback engine

---

## 📁 Project Structure

```text
Financial-Research-Agent/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── database.py
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   └── streamlit_app.py
│
├── .env
├── .gitignore
└── README.md

```
---
## ⚠️ Disclaimer

This project is built for educational purposes only.  
It does not provide financial advice or investment recommendations.
