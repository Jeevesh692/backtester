load_prices(path) takes a CSV path and returns a DataFrame sorted by time. It fails loudly if a column is missing.


total_return(equity) and max_drawdown(equity) each take a Series of account values and return a single number.

## Step 7.1 · Compose drill
- In Compose, services reach each other by name: `app` found `db` just by calling it "db" (no IPs needed).
- `docker compose down` removes containers but keeps named volumes (data survives); `down -v` deletes the volumes too.
- `depends_on` only waits for a container to start, not to be ready (use a healthcheck for that).