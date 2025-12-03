"""
Data Helpers for Money Talks

Provides functions for fetching and processing S&P 500 stock data using yfinance.
"""

import pandas as pd
import yfinance as yf
from pathlib import Path
from typing import Optional


def get_sp500_tickers() -> list[str]:
    """
    Get list of S&P 500 ticker symbols.

    Returns:
        List of ticker symbols (e.g., ['AAPL', 'MSFT', 'GOOGL', ...])

    Example:
        >>> tickers = get_sp500_tickers()
        >>> print(f"Found {len(tickers)} S&P 500 stocks")
    """
    # Try to load from local CSV first
    data_path = Path(__file__).parent.parent / "data" / "sp500_symbols.csv"

    if data_path.exists():
        df = pd.read_csv(data_path)
        return df["Symbol"].tolist()

    # Fallback: fetch from Wikipedia
    try:
        tables = pd.read_html(
            "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        )
        df = tables[0]
        return df["Symbol"].str.replace(".", "-", regex=False).tolist()
    except Exception:
        # Ultimate fallback: return major stocks
        return [
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B",
            "UNH", "JNJ", "JPM", "V", "PG", "XOM", "HD", "MA", "CVX", "MRK",
            "ABBV", "LLY", "PEP", "KO", "COST", "AVGO", "WMT", "MCD", "CSCO",
            "TMO", "ABT", "ACN", "DHR", "NEE", "NKE", "DIS", "VZ", "ADBE",
            "TXN", "PM", "CMCSA", "INTC", "WFC", "COP", "BMY", "UPS", "RTX"
        ]


def fetch_stock_data(
    ticker: str,
    period: str = "1y",
    interval: str = "1d"
) -> pd.DataFrame:
    """
    Fetch historical stock data for a single ticker.

    Args:
        ticker: Stock symbol (e.g., 'AAPL')
        period: Time period - 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        interval: Data interval - 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

    Returns:
        DataFrame with columns: Open, High, Low, Close, Volume, Dividends, Stock Splits

    Example:
        >>> df = fetch_stock_data("AAPL", period="6mo")
        >>> print(df.tail())
    """
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    return df


def fetch_multiple(
    tickers: list[str],
    period: str = "1y",
    interval: str = "1d"
) -> dict[str, pd.DataFrame]:
    """
    Fetch historical data for multiple tickers.

    Args:
        tickers: List of stock symbols
        period: Time period
        interval: Data interval

    Returns:
        Dictionary mapping ticker to DataFrame

    Example:
        >>> data = fetch_multiple(["AAPL", "MSFT", "GOOGL"])
        >>> for ticker, df in data.items():
        ...     print(f"{ticker}: {len(df)} rows")
    """
    result = {}
    for ticker in tickers:
        try:
            result[ticker] = fetch_stock_data(ticker, period, interval)
        except Exception as e:
            print(f"Warning: Could not fetch {ticker}: {e}")
    return result


def calculate_returns(
    df: pd.DataFrame,
    column: str = "Close",
    method: str = "simple"
) -> pd.Series:
    """
    Calculate returns from price data.

    Args:
        df: DataFrame with price data
        column: Column to use for calculation
        method: 'simple' for percentage returns, 'log' for log returns

    Returns:
        Series of returns

    Example:
        >>> df = fetch_stock_data("AAPL")
        >>> returns = calculate_returns(df)
        >>> print(f"Average daily return: {returns.mean():.4f}")
    """
    prices = df[column]

    if method == "simple":
        return prices.pct_change()
    elif method == "log":
        import numpy as np
        return np.log(prices / prices.shift(1))
    else:
        raise ValueError(f"Unknown method: {method}. Use 'simple' or 'log'.")


def get_stock_info(ticker: str) -> dict:
    """
    Get detailed information about a stock.

    Args:
        ticker: Stock symbol

    Returns:
        Dictionary with stock information (name, sector, market cap, etc.)

    Example:
        >>> info = get_stock_info("AAPL")
        >>> print(f"Company: {info.get('longName')}")
        >>> print(f"Sector: {info.get('sector')}")
    """
    stock = yf.Ticker(ticker)
    return stock.info


def get_market_cap_tier(ticker: str) -> str:
    """
    Classify a stock by market capitalization.

    Args:
        ticker: Stock symbol

    Returns:
        One of: 'Mega Cap', 'Large Cap', 'Mid Cap', 'Small Cap', 'Micro Cap'

    Example:
        >>> tier = get_market_cap_tier("AAPL")
        >>> print(f"AAPL is a {tier} stock")
    """
    info = get_stock_info(ticker)
    market_cap = info.get("marketCap", 0)

    if market_cap >= 200_000_000_000:  # $200B+
        return "Mega Cap"
    elif market_cap >= 10_000_000_000:  # $10B+
        return "Large Cap"
    elif market_cap >= 2_000_000_000:  # $2B+
        return "Mid Cap"
    elif market_cap >= 300_000_000:  # $300M+
        return "Small Cap"
    else:
        return "Micro Cap"


# Convenience function for Colab setup
def setup_colab():
    """
    Install required packages in Google Colab.

    Example:
        # Run this at the start of any Colab notebook
        from utils.data_helpers import setup_colab
        setup_colab()
    """
    try:
        import google.colab
        import subprocess
        subprocess.run(["pip", "install", "-q", "yfinance", "mplfinance"], check=True)
        print("Dependencies installed successfully!")
    except ImportError:
        print("Not running in Colab - skipping setup")
