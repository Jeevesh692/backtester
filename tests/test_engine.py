from backtester.engine import run
import pytest
import pandas as pd

@pytest.mark.parametrize(
    "signals, expected_trades",
    [
        (pd.Series([0] * 6), 0),
        (pd.Series([0, 0, 0, 0, 0, 1]), 0),
        (pd.Series([1] * 6), 1),
    ],
    ids=["never", "last_bar", "always"],
)
def test_trade_count(prices, signals, expected_trades):
    """The engine opens the expected number of trades for edge-case signal patterns."""
    equity, trades = run(prices, signals)
    assert len(trades) == expected_trades


def test_always_long_entry_and_exit(prices):
    """Always long: enter at bar 1's open, close at the last bar's close."""
    signals = pd.Series([1] * 6)
    equity, trades = run(prices, signals)
    assert len(trades) == 1
    assert trades[0]["entry_price"] == pytest.approx(1.1010)
    assert trades[0]["exit_price"] == pytest.approx(1.1035)



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

def test_entry_uses_next_bar_open_not_signal_bar_close(prices):
    """Guards against look-ahead: a signal on bar t fills at bar t+1's open, never bar t's close."""
    signals = pd.Series([0, 0, 1, 1, 0, 0])
    prices.loc[2, "close"] = 1.2000
    equity, trades = run(prices, signals)
    assert trades[0]["entry_price"] == pytest.approx(prices.loc[3, "open"]) 
    assert trades[0]["entry_price"] != pytest.approx(1.2000)


