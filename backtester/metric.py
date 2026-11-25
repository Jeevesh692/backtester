import pandas as pd

def total_return(equity: pd.Series) -> float:
    """
    Return the growth from the first to the last value, as a decimal (0.1 = 10%)" covers both.
    """
    equity_last = equity.iloc[-1]
    equity_open = equity.iloc[0]
    return (equity_last/equity_open) -1

def max_drawdown(equity: pd.Series) -> float:
    high_val = equity.cummax()
    min_val = equity.min()
    return ((min_val-high_val)/high_val)