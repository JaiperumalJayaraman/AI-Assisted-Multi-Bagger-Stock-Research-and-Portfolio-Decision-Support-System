# AI-Assisted Multi-Bagger Stock Research and Portfolio Decision Support System

A student-built research dashboard for exploring listed companies, reviewing available market data, comparing selected financial indicators, and modeling a hypothetical portfolio.

> **Important:** This repository currently contains an explainable, rule-based screening prototype—not a trained AI model or a reliable predictor of multi-bagger returns. Scores are research heuristics, not investment recommendations.

## Features

- **Market snapshot:** latest available adjusted close, recent price change, company/sector information, and selected valuation/fundamental indicators.
- **Price history:** interactive chart for a selectable historical period.
- **Explainable screening score:** weighted indicators for revenue growth, operating margin, debt/equity, forward P/E, and return on equity. Missing fields are excluded and the remaining weights are normalized.
- **Portfolio sandbox:** edit hypothetical quantities, average costs, and latest prices; view value and unrealized P/L; export holdings as CSV.
- **Research workflow:** practical prompts for deeper company analysis and risk review.

## Tech stack

- Python
- Streamlit — interactive web UI
- yfinance — market/company data access
- pandas — data handling
- Plotly — charts

## Run locally (Windows)

Install Python 3.10 or newer, then open PowerShell in the project folder:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501). An internet connection is required to fetch market data.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## How to use

1. Enter a ticker in the sidebar. Examples for Indian listings include `RELIANCE.NS`, `TCS.NS`, and `INFY.NS`; availability depends on the data provider.
2. Choose a historical price period.
3. Review the company snapshot, chart and factor-level screening table.
4. Use the portfolio sandbox for hypothetical holdings, not brokerage execution.
5. Export the sample holdings to CSV if needed for a report.

## Scoring methodology

The screening score uses these initial weights:

| Factor | Weight |
|---|---:|
| Revenue growth | 30% |
| Operating margin | 20% |
| Debt/equity | 20% |
| Forward P/E | 15% |
| Return on equity | 15% |

Each available factor is transformed onto a 0–100 heuristic scale using simple thresholds. The score is not a probability, forecast, or calibrated estimate of future returns. The method does not yet adjust for sector-specific norms, survivorship bias, data revisions, accounting quality, or point-in-time availability. Compare companies within appropriate sectors and verify all metrics against filings.

## Known limitations

- Market data is provided by Yahoo Finance through `yfinance`; availability, freshness, definitions, and coverage may vary. Some tickers/metrics may not resolve.
- Fundamentals may be missing or inconsistent; `N/A` does not mean zero or healthy.
- The portfolio table uses the prices entered by the user. It is not connected to a brokerage account and does not model taxes, fees, dividends, corporate actions, or currency conversion.
- This version does not ingest annual reports, summarize earnings calls, use an LLM, train a prediction model, or backtest a strategy. Those are planned extensions, not currently implemented features.

## Roadmap

1. Add company-universe screening with clear filters and sector-aware comparisons.
2. Add annual-report and earnings-call ingestion with source citations and risk/opportunity extraction.
3. Add a research memo template: thesis, catalysts, valuation, risks, and thesis-break conditions.
4. Build a reproducible historical dataset and leakage-aware backtesting pipeline before training and evaluating any prediction model.
5. Add tests, input validation, caching checks, and a deployment workflow.

## Disclaimer

This project is for education and research support only. It does not provide personalized financial advice, guarantee returns, or identify future multi-baggers with certainty. Verify data independently and consult a qualified professional before making investment decisions.
