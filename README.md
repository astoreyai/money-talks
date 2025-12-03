# Money Talks: Trading & Investing Education

A comprehensive 5-class trading and investing curriculum delivered through interactive Jupyter notebooks, designed for Google Colab.

## Overview

| Class | Topic | Lessons | Start Here |
|-------|-------|---------|------------|
| 1 | [Trading & Investing Fundamentals](class1_fundamentals/) | 20 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/astoreyai/money-talks/blob/main/class1_fundamentals/week1_market_basics/day01_what_are_markets.ipynb) |
| 2 | [Technical Indicators & Analysis](class2_technical_analysis/) | 20 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/astoreyai/money-talks/blob/main/class2_technical_analysis/week1_trend_indicators/day01_moving_averages.ipynb) |
| 3 | [Trading & Investing Strategies](class3_trading_strategies/) | 20 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/astoreyai/money-talks/blob/main/class3_trading_strategies/week1_active_trading/day01_day_trading_basics.ipynb) |
| 4 | [Taxes & Portfolio Maintenance](class4_taxes_portfolio/) | 20 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/astoreyai/money-talks/blob/main/class4_taxes_portfolio/week1_capital_gains/day01_intro_investment_taxes.ipynb) |
| 5 | [Trading Business & Advanced Topics](class5_trading_business/) | 20 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/astoreyai/money-talks/blob/main/class5_trading_business/week1_trader_tax_status/day01_intro_trader_tax.ipynb) |
| **Total** | | **100 notebooks** | |

**Format**: 30 min lecture + 15 min hands-on per lesson (45 min/day)
**Total Runtime**: 75 hours of instruction

## Quick Start

### Option 1: Google Colab (Recommended)
1. Navigate to any notebook in this repository
2. Click "Open in Colab" badge
3. Run the setup cell to install dependencies
4. Follow along with the lesson

### Option 2: Local Environment
```bash
git clone https://github.com/astoreyai/money-talks.git
cd money-talks
pip install -r requirements.txt
jupyter notebook
```

## Curriculum

### Class 1: Trading & Investing Fundamentals
Build a solid foundation in financial markets.

| Week | Topic | Key Concepts |
|------|-------|--------------|
| 1 | Market Basics | Markets, exchanges, hours, participants |
| 2 | Asset Classes | Stocks, bonds, ETFs, options/futures intro |
| 3 | Accounts & Orders | Brokerage accounts, order types |
| 4 | Charts & Psychology | Candlesticks, trading psychology |

### Class 2: Technical Indicators & Analysis
Master chart analysis and indicator interpretation.

| Week | Topic | Key Concepts |
|------|-------|--------------|
| 1 | Trend Indicators | Moving averages, crossovers |
| 2 | Momentum & Volatility | RSI, MACD, Bollinger Bands |
| 3 | Volume & Patterns | OBV, VWAP, chart patterns |
| 4 | Support/Resistance | S/R zones, Fibonacci, trendlines |

### Class 3: Trading & Investing Strategies
Strategy frameworks from day trading to long-term investing.

| Week | Topic | Key Concepts |
|------|-------|--------------|
| 1 | Active Trading | Day trading, scalping, momentum |
| 2 | Position & Trend | Trend following, breakouts |
| 3 | Value & Growth | Intrinsic value, dividends |
| 4 | Options Basics | Covered calls, puts, wheel strategy |

### Class 4: Taxes & Portfolio Maintenance
Critical knowledge for preserving and growing wealth.

| Week | Topic | Key Concepts |
|------|-------|--------------|
| 1 | Capital Gains | Short/long-term, cost basis |
| 2 | Tax-Advantaged | IRA, Roth, 401(k), HSA |
| 3 | Tax Optimization | Tax-loss harvesting, wash sales |
| 4 | Portfolio & Risk | Allocation, rebalancing, sizing |

### Class 5: Trading Business & Advanced Topics
Professional-level trading structures and automation.

| Week | Topic | Key Concepts |
|------|-------|--------------|
| 1 | Trader Tax Status | IRS criteria, TTS benefits |
| 2 | Trading Entities | LLC vs S-Corp, operating agreements |
| 3 | Mark-to-Market | Section 475(f), deductions |
| 4 | Compliance & Automation | PDT rules, algorithmic intro |

## Data Sources

All exercises use **S&P 500 stocks** via `yfinance`. No API keys required.

## Requirements

- Python 3.9+
- See `requirements.txt` for dependencies

## Project Structure

```
money-talks/
├── README.md
├── requirements.txt
├── class1_fundamentals/           # 20 notebooks
│   ├── week1_market_basics/
│   ├── week2_asset_classes/
│   ├── week3_accounts_orders/
│   └── week4_charts_psychology/
├── class2_technical_analysis/     # 20 notebooks
│   ├── week1_trend_indicators/
│   ├── week2_momentum_volatility/
│   ├── week3_volume_patterns/
│   └── week4_support_resistance/
├── class3_trading_strategies/     # 20 notebooks
│   ├── week1_active_trading/
│   ├── week2_position_trend/
│   ├── week3_value_growth/
│   └── week4_options_basics/
├── class4_taxes_portfolio/        # 20 notebooks
│   ├── week1_capital_gains/
│   ├── week2_tax_accounts/
│   ├── week3_tax_optimization/
│   └── week4_portfolio_risk/
├── class5_trading_business/       # 20 notebooks
│   ├── week1_trader_tax_status/
│   ├── week2_trading_entities/
│   ├── week3_mtm_deductions/
│   └── week4_compliance_automation/
├── utils/
│   ├── data_helpers.py
│   ├── chart_helpers.py
│   └── quiz_helpers.py
└── data/
    └── sp500_symbols.csv
```

## Contributing

This is an educational project. Issues and suggestions welcome.

## License

MIT License

## Disclaimer

**This content is for educational purposes only and does not constitute financial advice.**

- Past performance is not indicative of future results
- All investments involve risk, including the possible loss of principal
- The examples and strategies discussed are illustrative only
- Always consult with a qualified financial advisor before making investment decisions
- The authors and contributors are not responsible for any financial losses incurred

**Do your own research. Trade responsibly.**
