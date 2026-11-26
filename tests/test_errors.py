from backtester.data import load_prices
from backtester.strategy import ma_crossover
import pytest
import pandas as pd


def test_load_prices_names_missing_column(tmp_path):
    """load_prices raises ValueError naming the missing column when 'close' is absent."""
    csv_file = tmp_path / "bad.csv"         
    csv_file.write_text("time,open,high,low\n2024-01-01 00:00:00,1.1,1.2,1.0\n")
    with pytest.raises(ValueError, match="close"):
        load_prices(csv_file)
            


def test_ma_crossover_rejects_fast_not_below_slow():
    """ma_crossover raises ValueError when fast >= slow."""
    data = pd.DataFrame({"close": [1, 2, 3]})
    fast = 30
    slow = 10
    with pytest.raises(ValueError):
        ma_crossover(data,fast,slow)
        
