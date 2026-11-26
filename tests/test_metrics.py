import pandas as pd
import pytest

from backtester.metrics import max_drawdown, total_return

CURVE_IDS = ["flat", "rising", "dip"]


@pytest.mark.parametrize(
    "equity, expected",
    [
        (pd.Series([100, 100, 100]), 0.0),
        (pd.Series([100, 110, 120]), 0.2),
        (pd.Series([100, 120, 90, 110]), 0.1),
    ],
    ids=CURVE_IDS,
)
def test_total_return(equity, expected):
    """total_return matches hand-worked values for flat, rising and dipping curves."""
    assert total_return(equity) == pytest.approx(expected)


@pytest.mark.parametrize(
    "equity, expected",
    [
        (pd.Series([100, 100, 100]), 0.0),
        (pd.Series([100, 110, 120]), 0.0),
        (pd.Series([100, 120, 90, 110]), -0.25),
    ],
    ids=CURVE_IDS,
)
def test_max_drawdown(equity, expected):
    """max_drawdown matches hand-worked values for flat, rising and dipping curves."""
    assert max_drawdown(equity) == pytest.approx(expected)