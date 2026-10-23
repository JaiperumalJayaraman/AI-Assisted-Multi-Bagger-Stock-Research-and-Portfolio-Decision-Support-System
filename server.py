from __future__ import annotations

import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yfinance as yf
from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")

ALLOWED_PERIODS = {"6mo", "1y", "2y", "5y", "10y"}


def number(value: Any) -> float | None:
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (TypeError, ValueError):
        return None


def score_factor(value: Any, good: float, excellent: float, higher_is_better: bool = True) -> float | None:
    value = number(value)
    if value is None or excellent == good:
        return None
    if higher_is_better:
        raw_score = 50.0 + 50.0 * (value - good) / (excellent - good)
    else:
        raw_score = 50.0 + 50.0 * (good - value) / (good - excellent)
    return round(max(0.0, min(100.0, raw_score)), 1)


def analyse_info(info: dict[str, Any]) -> tuple[float | None, list[dict[str, Any]]]:
    factors = [
        ("Revenue growth", "revenueGrowth", 30, 0.05, 0.20, True, "percent"),
        ("Operating margin", "operatingMargins", 20, 0.05, 0.20, True, "percent"),
        ("Debt / equity", "debtToEquity", 20, 100, 30, False, "number"),
        ("Forward P/E", "forwardPE", 15, 35, 15, False, "multiple"),
        ("Return on equity", "returnOnEquity", 15, 0.08, 0.20, True, "percent"),
    ]
    weighted_total = 0.0
    available_weight = 0
    rows: list[dict[str, Any]] = []
    for label, key, weight, good, excellent, higher, kind in factors:
        raw = number(info.get(key))
        score = score_factor(raw, good, excellent, higher)
        if score is not None:
            weighted_total += score * weight
            available_weight += weight
        rows.append({
            "name": label,
            "key": key,
            "value": raw,
            "kind": kind,
            "weight": weight,
            "score": score,
        })
    total = round(weighted_total / available_weight, 1) if available_weight else None
    return total, rows


def stock_payload(ticker: str, period: str = "1y") -> dict[str, Any]:
    ticker = ticker.strip().upper()
    if not ticker or len(ticker) > 32:
        raise ValueError("Enter a valid stock ticker.")
    if period not in ALLOWED_PERIODS:
        period = "1y"

    stock = yf.Ticker(ticker)
    history = stock.history(period=period, auto_adjust=True)
    if history is None or history.empty or "Close" not in history:
        raise LookupError(f"No price history was found for {ticker}. Check the ticker and try again.")

    try:
        info = stock.get_info() or {}
    except Exception:
        info = {}

    closes = []
    for index, row in history.iterrows():
        close = number(row.get("Close"))
        if close is not None:
            try:
                date_label = index.strftime("%Y-%m-%d")
            except Exception:
                date_label = str(index)[:10]
            closes.append({"date": date_label, "close": close})

    if not closes:
        raise LookupError(f"No usable closing-price data was found for {ticker}.")

    latest_price = closes[-1]["close"]
    previous_price = closes[-2]["close"] if len(closes) > 1 else None
    change_pct = ((latest_price / previous_price) - 1) * 100 if previous_price else None
    score, factors = analyse_info(info)
    currency = info.get("currency") or "N/A"

    return {
        "ticker": ticker,
        "company": info.get("longName") or info.get("shortName") or ticker,
        "currency": currency,
        "latestPrice": latest_price,
        "changePct": change_pct,
        "marketCap": number(info.get("marketCap")),
        "revenueGrowth": number(info.get("revenueGrowth")),
        "operatingMargins": number(info.get("operatingMargins")),
        "debtToEquity": number(info.get("debtToEquity")),
        "forwardPE": number(info.get("forwardPE")),
        "returnOnEquity": number(info.get("returnOnEquity")),
        "sector": info.get("sector") or "Not available",
        "industry": info.get("industry") or "Not available",
        "summary": info.get("longBusinessSummary") or "No company summary is available from the current data provider.",
        "website": info.get("website") or "",
        "history": closes,
        "score": score,
        "factors": factors,
        "currencyNote": "Latest available data from Yahoo Finance. Quotes may be delayed or unavailable for some tickers.",
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Multi-Bagger Research Web App"})


@app.get("/api/stock")
def get_stock():
    ticker = request.args.get("ticker", "RELIANCE.NS")
    period = request.args.get("period", "1y")
    try:
        return jsonify(stock_payload(ticker, period))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except LookupError as exc:
        return jsonify({"error": str(exc)}), 404
    except Exception as exc:
        app.logger.exception("Stock lookup failed for %s", ticker)
        return jsonify({"error": "Could not load stock data. Check your internet connection and ticker, then try again."}), 502


@app.get("/api/compare")
def compare_stocks():
    raw = request.args.get("tickers", "RELIANCE.NS,TCS.NS,INFY.NS")
    tickers = list(dict.fromkeys(item.strip().upper() for item in raw.split(",") if item.strip()))[:8]
    if not tickers:
        return jsonify({"error": "Enter at least one ticker to compare."}), 400

    results = []
    for ticker in tickers:
        try:
            stock = stock_payload(ticker, "6mo")
            results.append({
                "ticker": stock["ticker"],
                "company": stock["company"],
                "currency": stock["currency"],
                "latestPrice": stock["latestPrice"],
                "changePct": stock["changePct"],
                "revenueGrowth": stock["revenueGrowth"],
                "operatingMargins": stock["operatingMargins"],
                "debtToEquity": stock["debtToEquity"],
                "forwardPE": stock["forwardPE"],
                "returnOnEquity": stock["returnOnEquity"],
                "score": stock["score"],
                "error": None,
            })
        except Exception as exc:
            results.append({"ticker": ticker, "company": ticker, "error": str(exc)})
    return jsonify({"results": results, "fetchedAt": datetime.now(timezone.utc).isoformat()})


if __name__ == "__main__":
    # Open http://127.0.0.1:5000 after starting this server.
    app.run(host="127.0.0.1", port=5000, debug=False)
