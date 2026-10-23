# AI-Assisted Multi-Bagger Stock Research and Portfolio Decision Support System

A student project for company research, market-data exploration, preliminary financial screening, and hypothetical portfolio tracking.

> **Important:** The current screening score is rule-based. It is not a trained AI prediction model and cannot reliably predict which stocks will become multi-baggers. This project is for education and research support, not personalized investment advice.

## Two ways to run the project

This repository contains both the original Streamlit prototype and a separate HTML web interface backed by Python/Flask.

### Option A — HTML website (Flask backend)

This starts the responsive HTML dashboard in your browser while the Python backend fetches stock information via `yfinance`.

**Windows (PowerShell):**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python server.py
```

Then open **http://127.0.0.1:5000** in your browser. Keep the terminal window open while using the site; it runs the backend that supplies market data. Do not double-click `index.html` directly, because the API endpoints require the Python server.

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python server.py
```

### Option B — Original Streamlit app

Use this if you prefer the original Python dashboard:

```powershell
streamlit run app.py
```

Streamlit usually opens at http://localhost:8501.

## Features currently implemented

- Latest available stock close and recent price movement.
- Historical adjusted-close chart for selected periods.
- Company summary, sector and industry when available.
- Financial metrics: revenue growth, operating margin, debt/equity, forward P/E, and return on equity.
- Explainable, rule-based screening score using available factors.
- Multi-stock comparison page in the HTML interface.
- Hypothetical portfolio tracker with editable quantity/cost, price refresh, unrealized P/L and CSV export.
- Responsive HTML, CSS and JavaScript interface, with Flask endpoints that retrieve data on the server side.

## Tech stack

- Python
- Flask — backend/API for the HTML site
- HTML, CSS and JavaScript — web interface
- Streamlit — alternative dashboard
- yfinance — Yahoo Finance market/company data access
- pandas — original Streamlit data handling
- Plotly — original Streamlit charting
- Chart.js — price chart in the HTML interface

## Example tickers

For Indian listings, try `RELIANCE.NS`, `TCS.NS` and `INFY.NS`. For US listings, examples include `AAPL` and `XYL`. Provider coverage can vary by symbol.

## Scoring methodology

The initial weighted factors are revenue growth (30%), operating margin (20%), debt/equity (20%), forward P/E (15%), and return on equity (15%). Each available metric is converted onto a 0–100 heuristic scale using simple thresholds, and the remaining factor weights are normalized when some data is missing.

This is a preliminary screen—not an estimate of the probability of future returns. The method does not yet account for sector-specific norms, survivorship bias, historical point-in-time availability, accounting quality, or data revisions. Validate values against filings before drawing conclusions.

## Known limitations

- Yahoo Finance data can be delayed, incomplete, or inconsistent. Some tickers and fundamentals will not resolve.
- The HTML site needs the Flask server running; opening `index.html` directly will not provide stock data.
- The portfolio is a local, hypothetical tracker, not connected to a brokerage account. It does not model fees, taxes, dividends, corporate actions, or currency conversion. Do not combine different currencies without conversion.
- The current version does not ingest annual reports, summarize earnings calls, use a large language model, train a predictive model, or backtest a strategy. These are possible future extensions, not current features.
- A working local server is not the same as a public deployed website. To share the HTML site publicly, deploy the Python backend to a suitable host; GitHub Pages alone cannot run the Flask/yfinance backend.

## Next steps

1. Test different tickers and all portfolio actions.
2. Add annual-report/earnings-call ingestion with citations and risk/opportunity extraction.
3. Add a research memo with thesis, catalysts, valuation, risks and thesis-break conditions.
4. Build point-in-time data and leakage-aware backtesting before evaluating any prediction model.
5. Add automated tests and a deployment workflow.

## Disclaimer

For educational use only. This software does not guarantee returns, predict future multi-baggers with certainty, or provide personalized financial advice. Independently verify data and consult a qualified professional before making investment decisions.
