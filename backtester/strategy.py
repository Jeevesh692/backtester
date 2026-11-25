import pandas as pd
def ma_crossover(prices: pd.DataFrame,fast:int,slow:int) -> pd.Series:
    """
    The function returns (1 when the fast MA of close is above the slow MA, otherwise 0) 
    and that the first bars are 0 because there's no average yet.
    """
    close_prices = prices["close"]
    fast_ma = close_prices.rolling(fast).mean()
    slow_ma = close_prices.rolling(slow).mean()
    bullish = fast_ma > slow_ma
    return bullish.astype("int64")