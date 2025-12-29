#!/usr/bin/env python3
"""Example usage of the finance project."""

from finance_project import Portfolio

def main():
    """Demonstrate portfolio functionality."""
    # Create a portfolio
    portfolio = Portfolio()

    # Add some stocks
    portfolio.add_stock('AAPL', 10)
    portfolio.add_stock('GOOGL', 5)
    portfolio.add_stock('MSFT', 8)

    # Display portfolio information
    print(f"Total portfolio value: ${portfolio.total_value():.2f}")
    print("Portfolio weights:")
    for ticker, weight in portfolio.portfolio_weights().items():
        print(f"  {ticker}: {weight:.2%}")

    print(f"Portfolio volatility: {portfolio.portfolio_volatility():.2%}")

if __name__ == "__main__":
    main()