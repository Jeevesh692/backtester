import backtester.__main__ as cli
def test_cli_prints_results_without_reading_disk(monkeypatch, capsys, prices):
    """The CLI prints its three results using mocked prices, never touching the file system."""
    monkeypatch.setattr(cli, "load_prices", lambda path: prices)
    cli.main(["ignored.csv", "--fast", "2", "--slow", "3"])
    captured = capsys.readouterr()
    assert "Trades" in captured.out