# AI Agent Instructions for Finance Project

## Architecture Overview
This is a Python-based financial analysis library with a modular architecture:

- **`finance_project/stock.py`**: Core `Stock` class for individual security data and analysis
- **`finance_project/portfolio.py`**: `Portfolio` class for managing collections of stocks
- **`finance_project/__init__.py`**: Package exports and version info

Data flows from Yahoo Finance API (via `yfinance`) through `Stock` objects to `Portfolio` calculations.

## Key Patterns & Conventions

### Stock Data Handling
- **Lazy loading**: Use `Stock.data` property instead of calling `fetch_data()` directly
- **Ticker normalization**: Always convert tickers to uppercase: `ticker.upper()`
- **Period defaults**: Use `"1y"` for historical data unless specified otherwise

### Financial Calculations
- **Annualization**: Use 252 trading days: `daily_returns.std() * (252 ** 0.5)`
- **Portfolio volatility**: Simple weighted average (no correlation adjustments)
- **Returns calculation**: `pct_change().dropna()` on closing prices

### Code Style
- **Type hints**: Use `typing` module for all function parameters and returns
- **Docstrings**: Include `Args:` and `Returns:` sections for public methods
- **Property access**: Prefer properties over direct attribute access (e.g., `stock.data`)

### Dependencies
Core stack: `pandas`, `numpy`, `yfinance`. Install via `pip install -r requirements.txt`.

## Development Workflow
```bash
# Install dependencies
pip install -r requirements.txt

# Run example
python Untitled-1.py
```

## Common Tasks
- **Add new stock**: `portfolio.add_stock('TICKER', quantity)`
- **Get current price**: `stock.current_price()`
- **Calculate weights**: `portfolio.portfolio_weights()`
- **Fetch data**: `stock.fetch_data(period="6mo")`

## File Organization
- `finance_project/`: Main package directory
- `requirements.txt`: Python dependencies
- `README.md`: Project documentation
- Example scripts in root directory