"""Portfolio management and analysis module."""

from typing import Dict, List
from .stock import Stock
import numpy as np


class Portfolio:
    """Manages a collection of stocks and portfolio analytics."""

    def __init__(self):
        """Initialize empty portfolio."""
        self.holdings: Dict[str, int] = {}  # ticker -> quantity
        self._stocks: Dict[str, Stock] = {}

    def add_stock(self, ticker: str, quantity: int):
        """Add shares of a stock to the portfolio.

        Args:
            ticker: Stock ticker symbol
            quantity: Number of shares to add
        """
        if ticker not in self.holdings:
            self.holdings[ticker] = 0
            self._stocks[ticker] = Stock(ticker)

        self.holdings[ticker] += quantity

    def remove_stock(self, ticker: str, quantity: int):
        """Remove shares of a stock from the portfolio.

        Args:
            ticker: Stock ticker symbol
            quantity: Number of shares to remove
        """
        if ticker in self.holdings:
            self.holdings[ticker] = max(0, self.holdings[ticker] - quantity)
            if self.holdings[ticker] == 0:
                del self.holdings[ticker]
                del self._stocks[ticker]

    def total_value(self) -> float:
        """Calculate total portfolio value."""
        total = 0.0
        for ticker, quantity in self.holdings.items():
            price = self._stocks[ticker].current_price()
            total += price * quantity
        return total

    def portfolio_weights(self) -> Dict[str, float]:
        """Calculate portfolio weights for each stock."""
        total_value = self.total_value()
        if total_value == 0:
            return {}

        weights = {}
        for ticker, quantity in self.holdings.items():
            price = self._stocks[ticker].current_price()
            weights[ticker] = (price * quantity) / total_value
        return weights

    def portfolio_volatility(self) -> float:
        """Calculate portfolio volatility using simple weighted average."""
        weights = self.portfolio_weights()
        volatilities = {ticker: self._stocks[ticker].volatility()
                       for ticker in self.holdings.keys()}

        # Simple weighted average (not accounting for correlations)
        portfolio_vol = 0.0
        for ticker, weight in weights.items():
            portfolio_vol += weight * volatilities[ticker]

        return portfolio_vol