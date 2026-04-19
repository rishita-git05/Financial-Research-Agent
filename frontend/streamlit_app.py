import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Indian Stock Analysis Assistant",
    page_icon="📈",
    layout="wide"
)


def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            try:
                return {"error": response.json().get("detail", "Something went wrong")}
            except Exception:
                return {"error": f"Request failed with status {response.status_code}"}
    except Exception as e:
        return {"error": f"Could not connect to backend: {str(e)}"}


def post_data(endpoint, params=None):
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            try:
                return {"error": response.json().get("detail", "Something went wrong")}
            except Exception:
                return {"error": f"Request failed with status {response.status_code}"}
    except Exception as e:
        return {"error": f"Could not connect to backend: {str(e)}"}


def delete_data(endpoint):
    try:
        response = requests.delete(f"{API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            try:
                return {"error": response.json().get("detail", "Something went wrong")}
            except Exception:
                return {"error": f"Request failed with status {response.status_code}"}
    except Exception as e:
        return {"error": f"Could not connect to backend: {str(e)}"}


def plot_price_chart(history_data, chart_title="Stock Price Chart", show_ma=True):
    if not isinstance(history_data, list) or len(history_data) == 0:
        st.warning("Historical price data not available")
        return

    df = pd.DataFrame(history_data)

    if "Date" not in df.columns or "Close" not in df.columns:
        st.warning("Historical data format is invalid")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df.dropna(subset=["Date", "Close"]).sort_values("Date")

    if df.empty:
        st.warning("No valid chart data available")
        return

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=df["Close"],
        mode="lines",
        name="Close Price"
    ))

    if show_ma:
        df["MA20"] = df["Close"].rolling(window=20).mean()
        df["MA50"] = df["Close"].rolling(window=50).mean()

        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df["MA20"],
            mode="lines",
            name="MA20"
        ))

        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df["MA50"],
            mode="lines",
            name="MA50"
        ))

    fig.update_layout(
        title=chart_title,
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)


def display_key_value_table(data: dict, title: str):
    if not data:
        st.info(f"No {title.lower()} available")
        return

    df = pd.DataFrame(
        [{"Metric": key.replace("_", " ").title(), "Value": value} for key, value in data.items()]
    )
    st.subheader(title)
    st.dataframe(df, use_container_width=True, hide_index=True)


def sentiment_score(sentiment: str):
    if sentiment == "Positive":
        return 1
    elif sentiment == "Negative":
        return -1
    return 0


def sentiment_description(sentiment: str):
    if sentiment == "Positive":
        return "Recent news tone appears optimistic, which may support investor confidence."
    elif sentiment == "Negative":
        return "Recent news tone appears pessimistic, which may indicate caution in market perception."
    return "Recent news tone appears balanced or mixed, with no strong positive or negative bias."


def display_sentiment_dashboard(sentiment: str):
    score = sentiment_score(sentiment)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": ""},
        title={"text": "Sentiment Score"},
        gauge={
            "axis": {"range": [-1, 1]},
            "bar": {"thickness": 0.3},
            "steps": [
                {"range": [-1, -0.1], "color": "#f8d7da"},
                {"range": [-0.1, 0.1], "color": "#fff3cd"},
                {"range": [0.1, 1], "color": "#d4edda"}
            ]
        }
    ))

    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric("News Sentiment", sentiment)

    with col2:
        st.info(sentiment_description(sentiment))

    st.plotly_chart(fig, use_container_width=True)


def generate_pdf_report(symbol, report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Financial Research Report", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Stock: {symbol}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=11)

    for line in report_text.split("\n"):
        clean_line = line.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 8, clean_line)

    return pdf.output(dest="S").encode("latin-1")


st.title("📊 Indian Stock Analysis Assistant")
st.markdown(
    "Analyze Indian stocks using technical indicators, news sentiment, fundamentals, watchlist, and portfolio tracking."
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "Stock Price",
        "Stock Analysis",
        "Fundamentals",
        "Stock Comparison",
        "Watchlist",
        "Portfolio",
        "Market Status"
    ]
)


# -----------------------------------
# 1. STOCK PRICE
# -----------------------------------
if menu == "Stock Price":
    st.header("Stock Price Lookup")

    symbol = st.text_input("Enter stock symbol", "TCS")
    period = st.selectbox("Select price history period", ["1mo", "3mo", "6mo", "1y"], index=0)

    if st.button("Get Stock Price"):
        result = fetch_data(f"/stocks/{symbol}")

        if "error" in result:
            st.error(result["error"])
        else:
            col1, col2, col3 = st.columns(3)
            col1.metric("Symbol", result.get("symbol"))
            col2.metric("Price", result.get("price"))
            col3.metric("Currency", result.get("currency"))

            details = {
                "Name": result.get("name"),
                "Market Cap": result.get("market_cap"),
                "Source": result.get("source")
            }
            display_key_value_table(details, "Stock Details")

            history = fetch_data(f"/stocks/{symbol}/history?period={period}")
            st.subheader("Price History Chart")
            plot_price_chart(
                history,
                chart_title=f"{result.get('symbol', symbol)} Price History",
                show_ma=False
            )


# -----------------------------------
# 2. STOCK ANALYSIS
# -----------------------------------
elif menu == "Stock Analysis":
    st.header("Full Stock Analysis")

    symbol = st.text_input("Enter stock symbol for analysis", "INFY")
    period = st.selectbox("Select history period", ["1mo", "3mo", "6mo", "1y"], index=1)

    if st.button("Analyze Stock"):
        result = fetch_data(f"/analysis/{symbol}")

        if "error" in result:
            st.error(result["error"])
        else:
            data = result.get("data", {})
            report = result.get("report", "")
            indicators = data.get("indicators", {})
            fundamentals = data.get("fundamentals", {})
            signals = data.get("signals", {})
            sentiment = data.get("sentiment", "Neutral")

            st.subheader(f"Analysis Summary: {data.get('symbol', symbol)}")

            # Top metrics
            top_metrics = st.columns(6)
            top_metrics[0].metric("Price", data.get("price"))
            top_metrics[1].metric("Trend", data.get("trend"))
            top_metrics[2].metric("RSI", indicators.get("RSI"))
            top_metrics[3].metric("Sentiment", sentiment)
            top_metrics[4].metric("Final Score", data.get("final_score", "N/A"))
            top_metrics[5].metric("Decision", data.get("final_decision", "N/A"))

            history = fetch_data(f"/stocks/{symbol}/history?period={period}")
            st.subheader("Interactive Stock Chart")
            plot_price_chart(
                history,
                chart_title=f"{data.get('symbol', symbol)} Price Chart with Moving Averages",
                show_ma=True
            )

            st.subheader("News Sentiment Dashboard")
            display_sentiment_dashboard(sentiment)

            col_a, col_b = st.columns(2)

            with col_a:
                display_key_value_table(indicators, "Technical Indicators")

            with col_b:
                display_key_value_table(signals, "Signal Summary")

            display_key_value_table(fundamentals, "Fundamental Overview")

            st.subheader("Generated Report")
            st.text_area("Analysis Report", report, height=350)

            st.subheader("AI Insights (Gemini)")
            ai_text = data.get("llm_analysis", "")

            if "unavailable" in ai_text.lower():
                st.warning(ai_text)
            else:
                st.success(ai_text)

            pdf_data = generate_pdf_report(data.get("symbol", symbol), report)

            st.download_button(
                label="Download PDF Report",
                data=pdf_data,
                file_name=f"{data.get('symbol', symbol)}_financial_report.pdf",
                mime="application/pdf"
            )


# -----------------------------------
# 3. FUNDAMENTALS
# -----------------------------------
elif menu == "Fundamentals":
    st.header("Fundamental Analysis")

    symbol = st.text_input("Enter stock symbol for fundamentals", "RELIANCE")

    if st.button("Get Fundamentals"):
        result = fetch_data(f"/fundamentals/{symbol}")

        if "error" in result:
            st.error(result["error"])
        else:
            if "fundamentals" in result:
                display_key_value_table(result["fundamentals"], "Fundamental Overview")
            else:
                display_key_value_table(result, "Fundamental Overview")


# -----------------------------------
# 4. STOCK COMPARISON
# -----------------------------------
elif menu == "Stock Comparison":
    st.header("Compare Stocks")

    symbols = st.text_input("Enter comma-separated stock symbols", "TCS,INFY,RELIANCE")

    if st.button("Compare"):
        result = fetch_data(f"/stocks/compare?symbols={symbols}")

        if "error" in result:
            st.error(result["error"])
        else:
            comparison = result.get("comparison", [])

            rows = []
            for item in comparison:
                data = item.get("data", {})
                fundamentals = data.get("fundamentals", {})
                rows.append({
                    "Symbol": data.get("symbol"),
                    "Price": data.get("price"),
                    "Trend": data.get("trend"),
                    "RSI": data.get("indicators", {}).get("RSI"),
                    "Sentiment": data.get("sentiment"),
                    "Final Score": data.get("final_score"),
                    "Decision": data.get("final_decision"),
                    "P/E": fundamentals.get("pe_ratio"),
                    "Market Cap": fundamentals.get("market_cap")
                })

            if rows:
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.warning("No comparison data available")


# -----------------------------------
# 5. WATCHLIST
# -----------------------------------
elif menu == "Watchlist":
    st.header("Watchlist")

    symbol = st.text_input("Enter stock symbol to add to watchlist", "HDFCBANK")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Add to Watchlist"):
            result = post_data(f"/watchlist/{symbol}")
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(result.get("message", "Added successfully"))

    with col2:
        if st.button("Refresh Watchlist"):
            st.rerun()

    watchlist_result = fetch_data("/watchlist/")

    if "error" in watchlist_result:
        st.error(watchlist_result["error"])
    else:
        watchlist = watchlist_result.get("watchlist", [])
        if watchlist:
            st.dataframe(pd.DataFrame(watchlist), use_container_width=True, hide_index=True)
        else:
            st.info("Watchlist is empty")

    remove_symbol = st.text_input("Enter stock symbol to remove from watchlist", "HDFCBANK")
    if st.button("Remove from Watchlist"):
        result = delete_data(f"/watchlist/{remove_symbol}")
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(result.get("message", "Removed successfully"))


# -----------------------------------
# 6. PORTFOLIO
# -----------------------------------
elif menu == "Portfolio":
    st.header("Portfolio Tracker")

    st.subheader("Add Stock to Portfolio")
    symbol = st.text_input("Stock symbol", "TCS")
    quantity = st.number_input("Quantity", min_value=1, value=10)
    buy_price = st.number_input("Buy Price", min_value=1.0, value=3500.0)

    if st.button("Add Stock to Portfolio"):
        result = post_data(
            "/portfolio/add",
            params={
                "symbol": symbol,
                "quantity": quantity,
                "buy_price": buy_price
            }
        )

        if "error" in result:
            st.error(result["error"])
        else:
            st.success(result.get("message", "Stock added successfully"))
            st.rerun()

    st.subheader("Current Portfolio Holdings")
    portfolio_result = fetch_data("/portfolio/")

    if "error" in portfolio_result:
        st.error(portfolio_result["error"])
    else:
        if portfolio_result:
            portfolio_df = pd.DataFrame(portfolio_result)
            st.dataframe(portfolio_df, use_container_width=True, hide_index=True)
        else:
            st.info("Portfolio is empty")

    st.subheader("Portfolio Summary")
    summary_result = fetch_data("/portfolio/summary")

    if "error" in summary_result:
        st.error(summary_result["error"])
    else:
        total_invested = summary_result.get("total_invested", 0)
        total_current = summary_result.get("total_current", 0)
        total_profit_loss = summary_result.get("total_profit_loss", 0)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Invested", total_invested)
        col2.metric("Total Current Value", total_current)
        col3.metric("Total Profit / Loss", total_profit_loss)
        col4.metric("Overall Return %", summary_result.get("overall_return_percent", 0))

        st.subheader("Portfolio Insights")

        insight_col1, insight_col2, insight_col3 = st.columns(3)

        best = summary_result.get("best_performer")
        worst = summary_result.get("worst_performer")
        diversification = summary_result.get("diversification_insight", "N/A")

        with insight_col1:
            if best:
                st.metric("Best Performer", f"{best['symbol']} ({best['profit_loss']})")
            else:
                st.metric("Best Performer", "N/A")

        with insight_col2:
            if worst:
                st.metric("Worst Performer", f"{worst['symbol']} ({worst['profit_loss']})")
            else:
                st.metric("Worst Performer", "N/A")

        with insight_col3:
            st.info(diversification)

        stocks_data = summary_result.get("stocks", [])

        if stocks_data:
            summary_df = pd.DataFrame(stocks_data)

            st.subheader("Detailed Portfolio Breakdown")
            st.dataframe(summary_df, use_container_width=True, hide_index=True)

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                if "current_value" in summary_df.columns and "symbol" in summary_df.columns:
                    pie_fig = go.Figure(
                        data=[
                            go.Pie(
                                labels=summary_df["symbol"],
                                values=summary_df["current_value"],
                                hole=0.4
                            )
                        ]
                    )
                    pie_fig.update_layout(title="Portfolio Allocation by Current Value")
                    st.plotly_chart(pie_fig, use_container_width=True)

            with chart_col2:
                if "profit_loss" in summary_df.columns and "symbol" in summary_df.columns:
                    bar_fig = go.Figure()
                    bar_fig.add_trace(go.Bar(
                        x=summary_df["symbol"],
                        y=summary_df["profit_loss"],
                        name="Profit/Loss"
                    ))
                    bar_fig.update_layout(
                        title="Profit / Loss by Stock",
                        xaxis_title="Stock",
                        yaxis_title="Profit / Loss"
                    )
                    st.plotly_chart(bar_fig, use_container_width=True)
        else:
            st.info("No summary data available")

    st.subheader("Portfolio Recommendations")
    rec_result = fetch_data("/portfolio/recommendations")

    if "error" in rec_result:
        st.error(rec_result["error"])
    else:
        if rec_result:
            rec_df = pd.DataFrame(rec_result)
            st.dataframe(rec_df, use_container_width=True, hide_index=True)

            if "decision" in rec_df.columns:
                decision_counts = rec_df["decision"].value_counts().reset_index()
                decision_counts.columns = ["Decision", "Count"]

                decision_fig = go.Figure()
                decision_fig.add_trace(go.Bar(
                    x=decision_counts["Decision"],
                    y=decision_counts["Count"],
                    name="Recommendation Count"
                ))
                decision_fig.update_layout(
                    title="Recommendation Distribution",
                    xaxis_title="Decision",
                    yaxis_title="Count"
                )
                st.plotly_chart(decision_fig, use_container_width=True)
        else:
            st.info("No recommendations available")

    st.subheader("Remove Stock from Portfolio")
    stock_id = st.number_input("Enter portfolio stock ID to delete", min_value=1, value=1)

    if st.button("Delete Portfolio Stock"):
        result = delete_data(f"/portfolio/{stock_id}")
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(result.get("message", "Deleted successfully"))
            st.rerun()


# -----------------------------------
# 7. MARKET STATUS
# -----------------------------------
elif menu == "Market Status":
    st.header("Indian Market Status")

    result = fetch_data("/stocks/market/status")

    if "error" in result:
        st.error(result["error"])
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Market", result.get("market"))
        col2.metric("Status", result.get("status"))
        col3.metric("Time", result.get("time"))

        st.info(result.get("message", ""))