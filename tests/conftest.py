import os
import pandas as pd
import pytest


@pytest.fixture
def prices():
    """Six hourly EURUSD bars built in memory, with hand-picked opens and closes."""
    data = {
        "time" : pd.date_range(start="2024-01-01", periods=6, freq = "h"),
        "open"  : [1.1000, 1.1010, 1.1020, 1.1030, 1.1050, 1.1040],
        "close" : [1.1005, 1.1015, 1.1025, 1.1045, 1.1045, 1.1035],
        "high"  : [1.1010, 1.1020, 1.1030, 1.1050, 1.1060, 1.1045],
        "low"   : [1.0995, 1.1005, 1.1015, 1.1025, 1.1040, 1.1030],
    }
    df = pd.DataFrame(data)
    return df


@pytest.fixture
def prices_csv(tmp_path, prices):
    """Write the prices fixture to a CSV in tmp_path and return its path."""
    path = tmp_path / "prices.csv"
    prices.to_csv(path, index=False)
    return path


@pytest.fixture
def in_tmp_dir(tmp_path):
    """Change into tmp_path for the test, then change back afterwards."""
    current_folder = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(current_folder)