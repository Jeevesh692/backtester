from backtester.engine import run
import pytest
import pandas as pd

def test_engine_sample(prices):
    """Hand-worked case: signals act on the next bar's open.

    Signals [0, 1, 1, 0, 0, 0] on 6 bars should give exactly one trade,
    entered and exited at the opens worked out by hand, with P&L
    (exit - entry) * 100,000 - 4.
    """
    signals = pd.Series([0, 1, 1, 0, 0, 0])
    equity, trades = run(prices,signals)
    assert len(trades) == 1
    assert trades[0]["pnl"] == pytest.approx(296)
    assert trades[0]["entry_price"] == pytest.approx(1.1020)
    assert trades[0]["exit_price"] == pytest.approx(1.1050)
