from backtester.data import load_prices

def test_load_sample():
    df = load_prices("data/sample.csv")
    assert set(df.columns) == {"time", "open", "high", "low", "close"}
    assert df["time"].is_monotonic_increasing 