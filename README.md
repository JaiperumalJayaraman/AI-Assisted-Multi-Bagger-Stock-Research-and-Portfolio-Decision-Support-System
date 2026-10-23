# AI-Assisted Multi-Bagger Stock Research and Portfolio Decision Support System

A student project for company research, market-data exploration, preliminary financial screening, and hypothetical portfolio tracking.

> **Important:** The current screening score is rule-based. It is not a trained AI prediction model and cannot reliably predict which stocks will become multi-baggers. This project is for education and research support, not personalized investment advice.

## Two ways to run the project

The repository contains the original Streamlit prototype and a separate HTML website backed by a Python/Flask API.

### Option A — Run the HTML website locally

The browser page needs the Python backend to fetch stock data. **Do not open `index.html` directly by double-clicking it**, and do not expect the GitHub file preview to work as the running app.

Install Python 3.10 or newer, then open PowerShell in the project folder:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python server.py
```

Keep the terminal window open, then open **http://127.0.0.1:5000** in the browser. The page and its API must run from the same Flask server.

### Option B — Publish it as a website using Render

A static-only host such as GitHub Pages cannot run the Flask/yfinance backend. This repository now has a `render.yaml` blueprint for a Python web service.

1. Sign in to Render and select **New → Blueprint**.
2. Connect the GitHub repository `JaiperumalJayaraman/AI-Assisted-Multi-Bagger-Stock-Research-and-Portfolio-Decision-Support-System`.
3. Review the service settings and deploy the blueprint.
4. Wait for deployment to finish, then open the HTTPS URL Render gives the service. That deployed URL is the one to share with teammates.

The hosting provider must run the Python backend; merely hosting the HTML file is not enough. Free-host behaviour and availability are controlled by the provider.

### Option C — Run the original Streamlit app

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
- Multi-stock comparison page in the HTML website.
- Hypothetical portfolio tracker with editable quantity/cost, price refresh, unrealized P/L and CSV export.
- Responsive HTML, CSS and JavaScript interface with Flask endpoints for market-data retrieval.

## Tech stack

- Python and Flask — backend/API for the HTML website
- HTML, CSS and JavaScript — browser interface
- Streamlit — alternative dashboard
- yfinance — Yahoo Finance market/company data access
- pandas and Plotly — original Streamlit app
- Chart.js — chart in the HTML interface
- Gunicorn — production WSGI server for hosting

## Example tickers

For Indian listings, try `RELIANCE.NS`, `TCS.NS` and `INFY.NS`. For US listings, examples include `AAPL` and `XYL`. Provider coverage can vary by symbol.

## Scoring methodology

The initial weighted factors are revenue growth (30%), operating margin (20%), debt/equity (20%), forward P/E (15%), and return on equity (15%). Each available metric is converted onto a 0–100 heuristic scale using simple thresholds, and the remaining factor weights are normalized when some data is missing.

This is a preliminary screen—not an estimate of the probability of future returns. The method does not yet account for sector-specific norms, survivorship bias, historical point-in-time availability, accounting quality, or data revisions. Validate values against filings before drawing conclusions.

## Known limitations

- Yahoo Finance data can be delayed, incomplete, or inconsistent. Some tickers and fundamentals will not resolve.
- The HTML site needs the Flask server running; opening `index.html` directly will not provide stock data.
- The portfolio is a local, hypothetical tracker, not connected to a brokerage account. It does not model fees, taxes, dividends, corporate actions, or currency conversion. Values are grouped by currency rather than converted.
- The current version does not ingest annual reports, summarize earnings calls, use a large language model, train a predictive model, or backtest a strategy. These are future extensions, not current features.

## Next steps

1. Test different tickers and all portfolio actions.
2. Add annual-report/earnings-call ingestion with citations and risk/opportunity extraction.
3. Add a research memo with thesis, catalysts, valuation, risks and thesis-break conditions.
4. Build point-in-time data and leakage-aware backtesting before evaluating any prediction model.
5. Add automated tests and monitoring.

## Disclaimer

For educational use only. This software does not guarantee returns, predict future multi-baggers with certainty, or provide personalized financial advice. Independently verify data and consult a qualified professional before making investment decisions.
