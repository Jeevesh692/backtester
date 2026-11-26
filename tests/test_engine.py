from backtester.engine import run
import pytest
import pandas as pd

def test_engine_sample():
    """Hand-worked case: signals act on the next bar's open.

    Signals [0, 1, 1, 0, 0, 0] on 6 bars should give exactly one trade,
    entered and exited at the opens worked out by hand, with P&L
    (exit - entry) * 100,000 - 4.
    """
    data = {
        "time" : pd.date_range(start="2024-01-01", periods=6, freq = "h"),
        "open"  : [1.1000, 1.1010, 1.1020, 1.1030, 1.1050, 1.1040],
        "close" : [1.1005, 1.1015, 1.1025, 1.1045, 1.1045, 1.1035]
    }
    df = pd.DataFrame(data)
    signals = pd.Series([0, 1, 1, 0, 0, 0])
    equity, trades = run(df,signals)
    assert len(trades) == 1
    assert trades[0]["pnl"] == pytest.approx(296)
    assert trades[0]["entry_price"] == pytest.approx(1.1020)
    assert trades[0]["exit_price"] == pytest.approx(1.1050)
