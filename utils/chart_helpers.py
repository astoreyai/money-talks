"""
Chart Helpers for Money Talks

Provides standardized visualization functions for stock market data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Optional, Literal


# Default style settings
STYLE = {
    "figure.figsize": (12, 6),
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.spines.top": False,
    "axes.spines.right": False,
}


def _apply_style():
    """Apply consistent styling to plots."""
    plt.rcParams.update(STYLE)


def plot_line(
    df: pd.DataFrame,
    column: str = "Close",
    title: str = "",
    ylabel: str = "Price ($)",
    figsize: tuple = (12, 6),
    color: str = "#2E86AB",
) -> plt.Figure:
    """
    Create a simple line chart of stock prices.

    Args:
        df: DataFrame with DatetimeIndex and price columns
        column: Column to plot
        title: Chart title
        ylabel: Y-axis label
        figsize: Figure size as (width, height)
        color: Line color

    Returns:
        matplotlib Figure

    Example:
        >>> df = fetch_stock_data("AAPL")
        >>> fig = plot_line(df, title="Apple Stock Price")
        >>> plt.show()
    """
    _apply_style()
    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(df.index, df[column], color=color, linewidth=1.5)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Date")

    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=45)

    plt.tight_layout()
    return fig


def plot_candlestick(
    df: pd.DataFrame,
    title: str = "",
    figsize: tuple = (12, 6),
    style: str = "yahoo",
) -> None:
    """
    Create a candlestick chart using mplfinance.

    Args:
        df: DataFrame with OHLC columns (Open, High, Low, Close) and DatetimeIndex
        title: Chart title
        figsize: Figure size
        style: mplfinance style ('yahoo', 'charles', 'mike', 'nightclouds', etc.)

    Example:
        >>> df = fetch_stock_data("AAPL", period="3mo")
        >>> plot_candlestick(df, title="AAPL - 3 Month Chart")
    """
    try:
        import mplfinance as mpf
    except ImportError:
        print("mplfinance not installed. Run: pip install mplfinance")
        return

    mpf.plot(
        df,
        type="candle",
        style=style,
        title=title,
        figsize=figsize,
        volume=True,
        ylabel="Price ($)",
        ylabel_lower="Volume",
    )


def plot_with_volume(
    df: pd.DataFrame,
    column: str = "Close",
    title: str = "",
    figsize: tuple = (12, 8),
) -> plt.Figure:
    """
    Create a price chart with volume bars below.

    Args:
        df: DataFrame with price and Volume columns
        column: Price column to plot
        title: Chart title
        figsize: Figure size

    Returns:
        matplotlib Figure

    Example:
        >>> df = fetch_stock_data("MSFT")
        >>> fig = plot_with_volume(df, title="Microsoft Price & Volume")
        >>> plt.show()
    """
    _apply_style()
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=figsize, gridspec_kw={"height_ratios": [3, 1]}, sharex=True
    )

    # Price chart
    ax1.plot(df.index, df[column], color="#2E86AB", linewidth=1.5)
    ax1.set_ylabel("Price ($)")
    ax1.set_title(title, fontsize=14, fontweight="bold")

    # Volume chart
    colors = ["#27AE60" if c >= o else "#E74C3C"
              for c, o in zip(df["Close"], df["Open"])]
    ax2.bar(df.index, df["Volume"], color=colors, alpha=0.7)
    ax2.set_ylabel("Volume")
    ax2.set_xlabel("Date")

    # Format x-axis
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=45)

    plt.tight_layout()
    return fig


def plot_with_indicator(
    df: pd.DataFrame,
    indicator: str,
    title: str = "",
    figsize: tuple = (12, 8),
    **indicator_params,
) -> plt.Figure:
    """
    Plot price with a technical indicator.

    Args:
        df: DataFrame with OHLC data
        indicator: One of 'sma', 'ema', 'bb' (Bollinger Bands), 'rsi'
        title: Chart title
        figsize: Figure size
        **indicator_params: Additional parameters for indicator calculation

    Returns:
        matplotlib Figure

    Example:
        >>> df = fetch_stock_data("GOOGL")
        >>> fig = plot_with_indicator(df, "sma", window=20)
        >>> plt.show()
    """
    _apply_style()

    indicator = indicator.lower()

    if indicator in ["sma", "ema"]:
        return _plot_moving_average(df, indicator, title, figsize, **indicator_params)
    elif indicator == "bb":
        return _plot_bollinger_bands(df, title, figsize, **indicator_params)
    elif indicator == "rsi":
        return _plot_rsi(df, title, figsize, **indicator_params)
    else:
        raise ValueError(f"Unknown indicator: {indicator}. Use 'sma', 'ema', 'bb', or 'rsi'")


def _plot_moving_average(
    df: pd.DataFrame,
    ma_type: str,
    title: str,
    figsize: tuple,
    window: int = 20,
) -> plt.Figure:
    """Plot price with moving average."""
    fig, ax = plt.subplots(figsize=figsize)

    # Calculate MA
    if ma_type == "sma":
        ma = df["Close"].rolling(window=window).mean()
        ma_label = f"SMA({window})"
    else:  # ema
        ma = df["Close"].ewm(span=window, adjust=False).mean()
        ma_label = f"EMA({window})"

    # Plot
    ax.plot(df.index, df["Close"], color="#2E86AB", linewidth=1.5, label="Close")
    ax.plot(df.index, ma, color="#E74C3C", linewidth=1.5, label=ma_label)

    ax.set_title(title or f"Price with {ma_label}", fontsize=14, fontweight="bold")
    ax.set_ylabel("Price ($)")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=45)

    plt.tight_layout()
    return fig


def _plot_bollinger_bands(
    df: pd.DataFrame,
    title: str,
    figsize: tuple,
    window: int = 20,
    num_std: float = 2.0,
) -> plt.Figure:
    """Plot price with Bollinger Bands."""
    fig, ax = plt.subplots(figsize=figsize)

    # Calculate Bollinger Bands
    sma = df["Close"].rolling(window=window).mean()
    std = df["Close"].rolling(window=window).std()
    upper = sma + (std * num_std)
    lower = sma - (std * num_std)

    # Plot
    ax.plot(df.index, df["Close"], color="#2E86AB", linewidth=1.5, label="Close")
    ax.plot(df.index, sma, color="#E74C3C", linewidth=1, label=f"SMA({window})")
    ax.fill_between(df.index, lower, upper, alpha=0.2, color="#E74C3C", label="Bollinger Bands")

    ax.set_title(title or f"Bollinger Bands ({window}, {num_std})", fontsize=14, fontweight="bold")
    ax.set_ylabel("Price ($)")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=45)

    plt.tight_layout()
    return fig


def _plot_rsi(
    df: pd.DataFrame,
    title: str,
    figsize: tuple,
    window: int = 14,
) -> plt.Figure:
    """Plot price with RSI indicator."""
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=figsize, gridspec_kw={"height_ratios": [2, 1]}, sharex=True
    )

    # Calculate RSI
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # Price chart
    ax1.plot(df.index, df["Close"], color="#2E86AB", linewidth=1.5)
    ax1.set_ylabel("Price ($)")
    ax1.set_title(title or f"Price with RSI({window})", fontsize=14, fontweight="bold")

    # RSI chart
    ax2.plot(df.index, rsi, color="#9B59B6", linewidth=1.5)
    ax2.axhline(70, color="#E74C3C", linestyle="--", alpha=0.7, label="Overbought (70)")
    ax2.axhline(30, color="#27AE60", linestyle="--", alpha=0.7, label="Oversold (30)")
    ax2.fill_between(df.index, 70, 100, alpha=0.1, color="#E74C3C")
    ax2.fill_between(df.index, 0, 30, alpha=0.1, color="#27AE60")
    ax2.set_ylabel("RSI")
    ax2.set_ylim(0, 100)
    ax2.legend(loc="upper right")

    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=45)

    plt.tight_layout()
    return fig


def compare_stocks(
    data: dict[str, pd.DataFrame],
    column: str = "Close",
    normalize: bool = True,
    title: str = "Stock Comparison",
    figsize: tuple = (12, 6),
) -> plt.Figure:
    """
    Compare multiple stocks on the same chart.

    Args:
        data: Dictionary mapping ticker to DataFrame
        column: Column to compare
        normalize: If True, normalize to percentage change from start
        title: Chart title
        figsize: Figure size

    Returns:
        matplotlib Figure

    Example:
        >>> data = fetch_multiple(["AAPL", "MSFT", "GOOGL"])
        >>> fig = compare_stocks(data, normalize=True)
        >>> plt.show()
    """
    _apply_style()
    fig, ax = plt.subplots(figsize=figsize)

    for ticker, df in data.items():
        values = df[column]
        if normalize:
            values = (values / values.iloc[0] - 1) * 100  # Percentage change
        ax.plot(df.index, values, linewidth=1.5, label=ticker)

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel("% Change" if normalize else "Price ($)")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=45)

    plt.tight_layout()
    return fig
