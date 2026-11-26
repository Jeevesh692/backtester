import pandas as pd
def ma_crossover(prices: pd.DataFrame,fast:int,slow:int) -> pd.Series:
    """Return a Series of 1/0 signals, one per bar.

    1 when the fast moving average of close is above the slow one, else 0.
    The first bars have no average yet (NaN) and are therefore 0.

    Raises:
        ValueError: if fast is not smaller than slow.
    """
    if fast >=slow:
        raise ValueError(f"Fast:{fast} must be lesser than slow:{slow}")
    close_prices = prices["close"]
    fast_ma = close_prices.rolling(fast).mean()
    slow_ma = close_prices.rolling(slow).mean()
    bullish = fast_ma > slow_ma
    return bullish.astype("int64")