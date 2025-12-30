"""Stock data and analysis module."""

import yfinance as yf
from typing import Optional
import pandas as pd


class Stock:
    """Represents a stock with historical data and analysis methods."""

    def __init__(self, ticker: str):
        """Initialize stock with ticker symbol.

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
        """
        self.ticker = ticker.upper()
        self._data: Optional[pd.DataFrame] = None

    def fetch_data(self, period: str = "1y") -> pd.DataFrame:
        """Fetch historical stock data.

        Args:
            period: Time period for data (e.g., '1y', '6mo', '1d')

        Returns:
            DataFrame with OHLCV data
        """
        self._data = yf.Ticker(self.ticker).history(period=period)
        return self._data

    @property
    def data(self) -> pd.DataFrame:
        """Get cached stock data, fetching if necessary."""
        if self._data is None:
            self.fetch_data()
        return self._data

    def current_price(self) -> float:
        """Get the most recent closing price."""
        return self.data['Close'].iloc[-1]

    def returns(self) -> pd.Series:
        """Calculate daily returns."""
        return self.data['Close'].pct_change().dropna()

    def volatility(self) -> float:
        """Calculate annualized volatility."""
        daily_returns = self.returns()
        return daily_returns.std() * (252 ** 0.5)  # 252 trading days