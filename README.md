# backtester

![CI](https://github.com/Jeevesh692/backtester/actions/workflows/ci.yml/badge.svg)

A small EURUSD backtester with no look-ahead. It runs a moving-average crossover on hourly bars, fills every signal at the next bar's open, and reports total return, max drawdown and trade count. Everything runs in Docker, and CI runs the full test suite on every push.

## Quick start

```bash
make build    # docker build -t backtester .
make run      # backtest data/sample.csv
```

Or locally with uv:

```bash
uv sync
uv run python -m backtester data/sample.csv --fast 10 --slow 30
```

## Running tests

```bash
make test             # inside Docker, same as CI
uv run pytest -q      # locally
uv run mutmut run     # mutation testing on metrics.py and engine.py
```

## Design decisions

- **Next-bar-open fills:** a signal on bar t's close is filled at bar t+1's open. A signal on the last bar is never filled.
- **Sizing and costs:** 1 lot (100,000 units) per trade, $4 per trade, $10,000 starting equity.
- **Open positions at the end:** closed at the last bar's close.
- **Max drawdown** is reported as a negative fraction (−0.25 = a 25% fall from the peak).
- **Look-ahead guard:** `test_entry_uses_next_bar_open_not_signal_bar_close` fails if the engine ever fills at the signal bar's close.

## Testing

- 17 tests: hand-worked metric and engine cases, edge cases, error paths, a mocked CLI test and the look-ahead guard.
- Mutation testing: 83% of mutants killed (91 of 109) in `metrics.py` and `engine.py`.

## Limitations

- One strategy (moving-average crossover), long only.
- No slippage, spread or swap; costs are a flat $4 per trade.
- Fixed 1-lot sizing.
