import yfinance as yf
import requests
import pandas as pd

# Alpha Vantage API Key
ALPHA_VANTAGE_API_KEY = 'DYTAVLTEK3UQB394'

# List of tickers to check
tickers = ['TSLA', 'AAPL', 'AMZN', 'META']

# Function to fetch and display labels from yfinance
def check_yfinance_labels(ticker):
    print(f"\nChecking yfinance data for {ticker}...")
    stock = yf.Ticker(ticker)
    
    # Financials
    print("Available Financials Index Labels:")
    print(stock.financials.index.tolist())

    # Balance Sheet
    print("\nAvailable Balance Sheet Index Labels:")
    print(stock.balance_sheet.index.tolist())

    # Cash Flow
    print("\nAvailable Cashflow Index Labels:")
    print(stock.cashflow.index.tolist())

    # Stock Info
    print("\nAdditional Stock Info Keys:")
    print(stock.info.keys())

# Function to fetch and display labels from Alpha Vantage
def check_alpha_vantage_labels(ticker):
    print(f"\nChecking Alpha Vantage data for {ticker}...")
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "OVERVIEW",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        print("\nAvailable Alpha Vantage Keys:")
        print(data.keys())
    except Exception as e:
        print(f"Error fetching Alpha Vantage data for {ticker}: {e}")

# Iterate over tickers and check labels
for ticker in tickers:
    check_yfinance_labels(ticker)
    check_alpha_vantage_labels(ticker)
