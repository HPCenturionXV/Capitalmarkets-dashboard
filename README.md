# Apex Dashboard

A professional-grade financial analytics platform built with Streamlit, featuring real-time market data, technical analysis, and institutional-grade visualizations.

## Features

- **Market Overview**: Real-time data for major indices (S&P 500, Dow Jones, NASDAQ, VIX)
- **Market Movers**: Top gainers and losers with detailed metrics
- **Stock Analysis**: Comprehensive technical analysis with charts and financial metrics
- **Professional UI**: Dark theme with institutional-grade styling
- **Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages
- **Rate Limiting**: Built-in protection against API rate limits

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run VeradashV6.py
```

## Deployment

This app is deployed on Streamlit Cloud and can be accessed at: [Your Streamlit Cloud URL]

## Data Sources

- Yahoo Finance API for real-time market data
- Built-in demo data fallback for rate limit scenarios

## Technologies Used

- Streamlit
- Plotly
- Pandas
- yfinance
- NumPy
