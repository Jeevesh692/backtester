from backtester.data import load_prices
from backtester.strategy import ma_crossover
import pytest
import pandas as pd


def test_load_prices_names_missing_column(tmp_path,prices):
    """load_prices raises ValueError naming the missing column when 'close' is absent."""
    path = tmp_path /"prices.csv"        
    prices.drop(columns="close").to_csv(path, index=False)
    with pytest.raises(ValueError, match="close"):
        load_prices(path)
            


def test_ma_crossover_rejects_fast_not_below_slow():
    """ma_crossover raises ValueError when fast >= slow."""
    data = pd.DataFrame({"close": [1, 2, 3]})
    fast = 30
    slow = 10
    with pytest.raises(ValueError):
        ma_crossover(data,fast,slow)
        
