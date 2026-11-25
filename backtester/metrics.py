import pandas as pd

def total_return(equity: pd.Series) -> float:
    """
    Return the growth from the first to the last value, as a decimal (0.1 = 10%)" covers both.
    """
    equity_last = equity.iloc[-1]
    equity_open = equity.iloc[0]
    return (equity_last/equity_open) -1

def max_drawdown(equity: pd.Series) -> float:
    """
    Returns thee max drawdown in negative decimal so -0.25 means -25%
    """
    high_val = equity.cummax()
    drawdown = (equity-high_val)/high_val
    return drawdown.min()