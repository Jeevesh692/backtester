"""Command-line entry point: python -m backtester <csv_path> [--fast N] [--slow N].

Loads prices, generates MA-crossover signals, runs the engine and prints
total return, max drawdown and the number of trades.

"""

import argparse

from backtester.data import load_prices
from backtester.engine import run
from backtester.metrics import max_drawdown, total_return
from backtester.strategy import ma_crossover

def main(argv=None):
    """
    Run the backtest from the command line and print total return, max drawdown and trade count.
    """

    parser = argparse.ArgumentParser(description="Backtest a moving-average crossover strategy on a price CSV.")
    parser.add_argument("csv_path", help="Path to a CSV with time, open, high, low, close columns.")
    parser.add_argument("--fast", type=int, default=10, help="Fast moving-average window in bars (default: 10).")
    parser.add_argument("--slow", type=int, default=30, help="Slow moving-average window in bars (default: 30).")
    args = parser.parse_args(argv)

    prices = load_prices(args.csv_path)
    signals = ma_crossover(prices, args.fast, args.slow)
    equity, trades = run(prices, signals)

    print(f"Total return: {total_return(equity):.2%}")
    print(f"Max drawdown: {max_drawdown(equity):.2%}")
    print(f"Trades:       {len(trades)}")

if __name__ == "__main__":
    
    main()
    