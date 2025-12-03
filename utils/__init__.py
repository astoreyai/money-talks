"""
Money Talks Utility Modules

Provides helper functions for:
- data_helpers: Fetching and processing market data
- chart_helpers: Standardized visualizations
- quiz_helpers: Interactive quiz widgets
"""

from .data_helpers import (
    get_sp500_tickers,
    fetch_stock_data,
    fetch_multiple,
    calculate_returns,
)

from .chart_helpers import (
    plot_candlestick,
    plot_line,
    plot_with_volume,
    plot_with_indicator,
)

from .quiz_helpers import (
    multiple_choice,
    true_false,
    Quiz,
)

__all__ = [
    # Data helpers
    "get_sp500_tickers",
    "fetch_stock_data",
    "fetch_multiple",
    "calculate_returns",
    # Chart helpers
    "plot_candlestick",
    "plot_line",
    "plot_with_volume",
    "plot_with_indicator",
    # Quiz helpers
    "multiple_choice",
    "true_false",
    "Quiz",
]
