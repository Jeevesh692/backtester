# NOTES — backtester

## Module contracts (what goes in, what comes out)
- `load_prices(path)` takes a CSV path and returns a DataFrame sorted by time. It fails loudly (`ValueError` naming the columns) if any of `time, open, high, low, close` is missing.
- `total_return(equity)` and `max_drawdown(equity)` each take a Series of account values and return a single number (a decimal: 0.10 = 10%).
- `ma_crossover(prices, fast, slow)` takes the prices DataFrame and two window sizes, and returns a Series of 1/0 signals (one per bar). Raises `ValueError` if `fast >= slow`.
- `run(prices, signals, cost_per_trade=4.0)` takes prices and signals, and returns `(equity, trades)`: an equity Series indexed by time and a list of trade dicts (`entry_time, exit_time, entry_price, exit_price, pnl`).
- `__main__.py` connects them: argparse → `load_prices` → `ma_crossover` → `run` → prints total return, max drawdown and trade count.

## Decisions I made
- **Drawdown sign:** negative. −0.25 means the account fell 25% below its running peak, so `max_drawdown` uses `.min()`.
- **Next-bar-open fills:** a signal on bar t is traded at bar t+1's open. Using bar t's close would be look-ahead bias (trading on a price I couldn't have known yet).
- **End-of-data rule:** if still long on the last bar, the trade is closed at the last bar's close and recorded, so the trades list and final equity agree.
- **Trade maths:** 1 lot = 100,000 units, $4 cost per trade, $10,000 start. P&L = (exit − entry) × 100,000 − 4.

