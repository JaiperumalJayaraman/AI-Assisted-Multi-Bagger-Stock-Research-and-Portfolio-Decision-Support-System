from __future__ import annotations

import math
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Multi-Bagger Research Lab", page_icon="📈", layout="wide")

st.title("📈 AI-Assisted Multi-Bagger Stock Research & Portfolio Decision Support")
st.caption("Research support for exploring business quality, growth, valuation and portfolio risk. Scores are screening heuristics—not predictions or investment advice.")

with st.sidebar:
    st.header("Research settings")
    ticker_input = st.text_input("Stock ticker", value="RELIANCE.NS", help="Examples: RELIANCE.NS, TCS.NS, INFY.NS, AAPL")
    history_period = st.selectbox("Price history", ["6mo", "1y", "2y", "5y", "10y"], index=2)
    st.markdown("---")
    st.caption("Data is supplied by Yahoo Finance via yfinance. Availability, coverage and accuracy can vary by market and ticker.")

@st.cache_data(ttl=900, show_spinner=False)
def load_data(ticker: str, period: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    stock = yf.Ticker(ticker.strip())
    history = stock.history(period=period, auto_adjust=True)
    try:
        info = stock.get_info()
    except Exception:
        info = {}
    return history, info or {}

def fmt_num(value: Any, suffix: str = "", digits: int = 2) -> str:
    try:
        if value is None or not math.isfinite(float(value)):
            return "N/A"
        return f"{float(value):,.{digits}f}{suffix}"
    except (TypeError, ValueError):
        return "N/A"

def score_component(value: Any, good: float, excellent: float, higher_is_better: bool = True) -> float | None:
    try:
        x = float(value)
        if not math.isfinite(x):
            return None
        if higher_is_better:
            return max(0.0, min(100.0, 50.0 + 50.0 * (x - good) / (excellent - good)))
        return max(0.0, min(100.0, 50.0 + 50.0 * (good - x) / (good - excellent)))
    except (TypeError, ValueError, ZeroDivisionError):
        return None

def build_score(info: dict[str, Any]) -> tuple[float | None, pd.DataFrame]:
    metrics = [
        ("Revenue growth", "revenueGrowth", 30, 0.05, 0.20, True, "%"),
        ("Profitability (operating margin)", "operatingMargins", 20, 0.05, 0.20, True, "%"),
        ("Financial health (debt/equity)", "debtToEquity", 20, 100, 30, False, ""),
        ("Valuation (forward P/E)", "forwardPE", 15, 35, 15, False, "x"),
        ("Capital efficiency (ROE)", "returnOnEquity", 15, 0.08, 0.20, True, "%"),
    ]
    rows = []
    weighted_points = 0.0
    available_weight = 0.0
    for label, key, weight, good, excellent, higher, unit in metrics:
        raw = info.get(key)
        # Yahoo Finance sometimes reports debt/equity as percentage points and ratios as decimals.
        score = score_component(raw, good, excellent, higher)
        if score is not None:
            weighted_points += score * weight
            available_weight += weight
        display = fmt_num(raw * 100 if unit == "%" and raw is not None else raw, "%" if unit == "%" else ("x" if unit == "x" else ""))
        rows.append({"Factor": label, "Available data": display, "Weight": f"{weight}%", "Factor score": f"{score:.0f}/100" if score is not None else "N/A"})
    total = weighted_points / available_weight if available_weight else None
    return total, pd.DataFrame(rows)

try:
    with st.spinner("Fetching market and company data…"):
        history, info = load_data(ticker_input, history_period)
    if history.empty:
        st.error("No price history was returned. Check the ticker symbol or try another one.")
        st.stop()
except Exception as exc:
    st.error(f"Unable to load market data: {exc}")
    st.info("Check your internet connection and ticker symbol. You can still inspect the project source on GitHub.")
    st.stop()

company = info.get("longName") or info.get("shortName") or ticker_input.upper()
latest_price = history["Close"].dropna().iloc[-1] if not history["Close"].dropna().empty else None
previous_price = history["Close"].dropna().iloc[-2] if history["Close"].dropna().shape[0] > 1 else None
change_pct = ((latest_price / previous_price) - 1) * 100 if latest_price and previous_price else None
score, factor_table = build_score(info)

st.subheader(f"{company} ({ticker_input.upper()})")
a, b, c, d = st.columns(4)
a.metric("Latest close", fmt_num(latest_price, f" {info.get('currency', '')}"), f"{change_pct:+.2f}%" if change_pct is not None else None)
b.metric("Market capitalization", fmt_num((info.get("marketCap") or 0) / 1e7, " Cr" if info.get("currency") == "INR" else "", 1) if info.get("marketCap") else "N/A")
c.metric("Revenue growth", fmt_num((info.get("revenueGrowth") * 100) if info.get("revenueGrowth") is not None else None, "%"))
d.metric("Research screen score", f"{score:.0f}/100" if score is not None else "Insufficient data")

left, right = st.columns([1.65, 1])
with left:
    st.markdown("### Historical price")
    fig = px.line(history.reset_index(), x="Date", y="Close", title=f"{ticker_input.upper()} adjusted closing price")
    fig.update_layout(xaxis_title="Date", yaxis_title=f"Price ({info.get('currency', 'currency units')})", margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.markdown("### Company snapshot")
    st.write(info.get("longBusinessSummary") or "No company summary is available from the data provider.")
    st.caption(f"Sector: {info.get('sector', 'N/A')} · Industry: {info.get('industry', 'N/A')}")

st.markdown("### Explainable screening factors")
st.dataframe(factor_table, use_container_width=True, hide_index=True)
st.caption("The score averages only the factors with available data and renormalizes their weights. It is a prioritization heuristic, not a probability of becoming a multi-bagger. Sector differences and accounting quality require human review.")

st.markdown("### Portfolio sandbox")
st.write("Enter hypothetical holdings to calculate basic portfolio value and unrealized P/L. These values are not linked to a brokerage account.")
if "holdings" not in st.session_state:
    st.session_state.holdings = pd.DataFrame([{"Ticker": ticker_input.upper(), "Quantity": 10.0, "Average cost": 100.0, "Latest price": float(latest_price or 0.0)}])
holdings = st.data_editor(st.session_state.holdings, num_rows="dynamic", use_container_width=True, key="holdings_editor")
for col in ["Quantity", "Average cost", "Latest price"]:
    if col in holdings:
        holdings[col] = pd.to_numeric(holdings[col], errors="coerce").fillna(0)
holdings["Invested value"] = holdings.get("Quantity", 0) * holdings.get("Average cost", 0)
holdings["Current value"] = holdings.get("Quantity", 0) * holdings.get("Latest price", 0)
holdings["Unrealized P/L"] = holdings["Current value"] - holdings["Invested value"]
total_cost = holdings["Invested value"].sum()
total_value = holdings["Current value"].sum()
pl = total_value - total_cost
p, q, r = st.columns(3)
p.metric("Invested value", fmt_num(total_cost, ""))
q.metric("Current value", fmt_num(total_value, ""))
r.metric("Unrealized P/L", fmt_num(pl, ""), fmt_num((pl / total_cost * 100) if total_cost else None, "%"))
st.dataframe(holdings, use_container_width=True, hide_index=True)
st.download_button("Download holdings as CSV", holdings.to_csv(index=False).encode("utf-8"), file_name="portfolio_holdings.csv", mime="text/csv")

st.markdown("### Research workflow")
st.markdown("1. Screen candidates with comparable financial indicators.\n2. Read annual reports and earnings-call transcripts.\n3. Investigate industry structure, addressable market, management quality, dilution and governance.\n4. Document a bull case, bear case, valuation range and thesis-break conditions.\n5. Backtest any predictive method with point-in-time data and out-of-sample evaluation before making claims about performance.")
st.warning("Educational prototype only. Scores and market data can be incomplete or delayed. This application does not predict returns or provide personalized investment advice.")
