import pandas as pd


def run(prices: pd.DataFrame, signals: pd.Series, cost_per_trade: float = 4.0) -> tuple[pd.Series, list[dict]]:
    """Simulate a long-only strategy bar by bar.

    Rules:
    - The signal on bar t is acted on at bar t+1's open (no look-ahead).
    - 1 lot = 100,000 units; each trade costs cost_per_trade dollars.
    - Start with $10,000. Equity = 10,000 + closed P&L + open P&L,
      with open P&L marked at each bar's close.
    - A trade still open on the last bar is closed at the last close.

    Returns (equity, trades): equity is a Series indexed by time;
    trades is a list of dicts with entry_time, exit_time,
    entry_price, exit_price and pnl.
    """
    units = 100_000
    opens = prices["open"]
    closes = prices["close"]
    times = prices["time"]

    cash = 10_000.0          # starting money + CLOSED P&L only
    in_position = False
    entry_price = None
    entry_time = None
    trades = []
    equity_curve = []

    for i in range(len(prices)):
        # 1. Act at this bar's open, using the PREVIOUS bar's signal
        if i > 0:
            prev_signal = signals.iloc[i - 1]
            if prev_signal == 1 and not in_position:
                in_position = True
                entry_price = opens.iloc[i]
                entry_time = times.iloc[i]
            elif prev_signal == 0 and in_position:
                exit_price = opens.iloc[i]
                pnl = (exit_price - entry_price) * units - cost_per_trade
                cash += pnl
                trades.append({
                    "entry_time": entry_time,
                    "exit_time": times.iloc[i],
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "pnl": pnl,
                })
                in_position = False

        # 2. Last bar: force-close any open trade at the close
        if i == len(prices) - 1 and in_position:
            exit_price = closes.iloc[i]
            pnl = (exit_price - entry_price) * units - cost_per_trade
            cash += pnl
            trades.append({
                "entry_time": entry_time,
                "exit_time": times.iloc[i],
                "entry_price": entry_price,
                "exit_price": exit_price,
                "pnl": pnl,
            })
            in_position = False

        # 3. Mark equity at this bar's close
        if in_position:
            open_pnl = (closes.iloc[i] - entry_price) * units
        else:
            open_pnl = 0.0
        equity_curve.append(cash + open_pnl)

    equity = pd.Series(equity_curve, index=times, name="equity")
    return equity, trades