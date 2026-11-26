from backtester.data import load_prices


def test_load_prices_relative_path(in_tmp_dir, prices_csv):
    """load_prices works with a path relative to the current folder."""
    df = load_prices("prices.csv")
    assert len(df) == 6
