# NOTES — backtester

## Module contracts (what goes in, what comes out)
- `load_prices(path)` takes a CSV path and returns a DataFrame sorted by time. It fails loudly (`ValueError` naming the columns) if any of `time, open, high, low, close` is missing.
- `total_return(equity)` and `max_drawdown(equity)` each take a Series of account values and return a single number (a decimal: 0.10 = 10%).
- `ma_crossover(prices, fast, slow)` takes the prices DataFrame and two window sizes, and returns a Series of 1/0 signals (one per bar). Raises `ValueError` if `fast >= slow`.
- `run(prices, signals, cost_per_trade=4.0)` takes prices and signals, and returns `(equity, trades)`: an equity Series indexed by time and a list of trade dicts (`entry_time, exit_time, entry_price, exit_price, pnl`).
- `__main__.py` connects them: argparse → `load_prices` → `ma_crossover` → `run` → prints total return, max drawdown and trade count.

## Decisions I made
- **Drawdown sign:** negative. −0.25 means the account fell 25% below its running peak, so `max_drawdown` uses `.min()`.
- **Next-bar-open fills:** a signal on bar t is traded at bar t+1's open. Using bar t's close would be look-ahead bias (trading on a price I couldn't have known yet).
- **End-of-data rule:** if still long on the last bar, the trade is closed at the last bar's close and recorded, so the trades list and final equity agree.
- **Trade maths:** 1 lot = 100,000 units, $4 cost per trade, $10,000 start. P&L = (exit − entry) × 100,000 − 4.

---

## Step 6 · Setup, data and metrics

### Workbench
- **WSL + Ubuntu:** real Linux inside Windows, the same kind of system my code and containers run on.
- **VS Code must say "WSL: Ubuntu"** in the bottom-left, or it uses Windows Python and paths.
- **Keep code in `~/code` (Linux side),** not on the Windows drive (`/mnt/c/...`), which is slow and causes permission problems.
- **SSH key** lets me push to GitHub without typing a password.

### Repo setup
- `git init` starts history; branch `main` matches GitHub's default.
- `git config user.name / user.email`: every commit is stamped with these. Email must match GitHub.
- **venv** = private Python for this project. `source .venv/bin/activate` each new terminal; `(.venv)` shows it's on.
- Ubuntu needed `python3.x-venv` installed separately before `python3 -m venv` worked.
- Git **U** = untracked (never committed), **M** = modified since last commit.

### Project files
- `backtester/` + `__init__.py` = the package, so `from backtester.data import ...` works.
- `tests/`: pytest finds files and functions starting with `test_`.
- `.gitignore`: keeps `.venv/`, `__pycache__/` and `.pytest_cache/` out of git.
- `requirements.txt`: the package list; `pip install -r requirements.txt`.
- `pytest.ini` with `pythonpath = .`: lets tests `import backtester`.
- Dot-names (`.venv`, `.git`, `.pytest_cache`) are **hidden folders**, made by tools. See them with `ls -a`.

### Making sample.csv from the MT5 export
- The export was `.gz` (compressed), tab-separated, with date and time in separate columns and dots in dates.
- `zcat file.gz | head -n 301 | awk '...' > data/sample.csv` — decompress, take 301 lines, reshape with awk.
- Paths with spaces need quotes.

### Python lessons
- `.iloc[0]` / `.iloc[-1]` = first / last value by position.
- `Series.cummax()` = running peak. Drawdown = (equity − peak) / peak.
- **Vectorisation:** maths between two Series runs element by element, no loop needed.
- Type hints (`-> float`) are notes for readers and editors; Python doesn't enforce them.
- Don't name a variable the same as a function (`total_return = total_return(...)`).
- Operator precedence: `a - b / c` divides first. Use brackets.

---

## Step 7 · Docker Compose

### Terminal vs YAML
- `docker ...` / `docker compose ...` commands run in the **terminal** (docker is just another program, like git).
- `docker-compose.yml` is a **description**, not commands. Compose reads it and runs Docker for me.
- The YAML is like a long `docker run` saved in a file:
  `image` = image name · `volumes` = `-v` · `environment` = `-e` · `ports` = `-p` · `working_dir` = `-w` · `command` = the command at the end.

### YAML rules
- Indentation shows what belongs to what. **Spaces only, never tabs**, and be consistent.
- `key: value` = one setting. A line starting with `- ` = one item in a **list**.
- Lists needed for: `volumes`, `depends_on`.
- Key names must be exact: `command`, `depends_on`, `working_dir`.

### Key ideas
- **Services reach each other by name.** In the drill, `app` found `db` just by calling it "db" (no IPs needed).
- **Inside vs outside the container.** The container is its own little Linux machine. Paths on my laptop (`/home/jeevesh_prakash/...`) don't exist inside it.
- **Named volume** (`pgdata:/var/lib/postgresql/data`) = storage Docker manages; data survives the container. Must also be declared under a top-level `volumes:` key.
- **Bind mount** (`.:/app`) = my laptop folder shown inside the container. Format: `laptop-path:container-path`. No top-level `volumes:` needed.
- `working_dir` = the folder *inside the container* where the command starts (like `cd /app`). Must be a folder, not a file.
- `depends_on` only waits for a container to **start**, not to be **ready** (a healthcheck handles that).
- `sh -c "a && b"` runs two commands; `&&` runs b only if a succeeded.

### Commands
- `docker compose up`: start everything (Ctrl+C to stop).
- `docker compose down`: remove containers + network, **keep** volumes.
- `docker compose down -v`: also **delete** volumes (data gone).
- `docker compose run --rm tests`: run one service once, delete the container after.
- `docker volume ls`: list volumes.

---

## Step 8 · Strategy, engine and CLI

### Strategy
- `Series.rolling(n).mean()` = moving average. First n−1 bars are NaN; comparing with NaN gives False, so those bars become 0.
- `.astype(int)` turns True/False into 1/0.
- The strategy takes `prices` as a parameter; it doesn't load files. Each module has one job, which makes testing easy.

### Engine
- Loop over **positions**: `for i in range(len(prices))` (not `for i in signals`, which loops over values).
- Bar 0 has no previous signal. `signals.iloc[-1]` would wrap round to the **last** signal, so skip trading on bar 0.
- Order inside each bar: act at the open → force-close on the last bar → mark equity at the close.
- `cash` holds only 10,000 + **closed** P&L. Open P&L is recalculated each bar and added only when recording equity.
- Don't name variables `open` or `time` (`open` is a built-in function).

### CLI (`__main__.py`)
- `python -m backtester` runs the package's `__main__.py`.
- **argparse:** `add_argument("csv_path")` = required positional; `add_argument("--fast", type=int, default=10)` = optional. `args` only contains what I defined.
- `type=int` matters: everything typed in a terminal arrives as text.
- `f"{value:.2%}"` prints 0.1 as `10.00%`.

### Hand-worked engine test
- Signals `[0, 1, 1, 0, 0, 0]` → enter at bar 2's open (1.1020), exit at bar 4's open (1.1050), P&L = 0.0030 × 100,000 − 4 = **296**.
- `pytest.approx` for floats: 1.1050 − 1.1020 isn't exactly 0.003 in a computer.
- Check prices as well as P&L: a bug could shift entry and exit and still give a similar P&L.

---

## Step 9 · Dockerfile, .dockerignore, Makefile

### Dockerfile
- A recipe for **my own image**. File named exactly `Dockerfile` (no extension).
- `FROM` start image → `WORKDIR /app` → `COPY requirements` → `RUN pip install` → `COPY . .` → `CMD`.
- **`RUN` = build time** (baked into the image). **`CMD` = run time** (every time a container starts).
- `CMD ["python", "-m", "backtester", "data/sample.csv"]`: JSON form runs the program directly, no shell in between.
- `ENV PYTHONDONTWRITEBYTECODE=1` = no `.pyc` files; `PYTHONUNBUFFERED=1` = prints show immediately.

### Layer caching
- Each instruction = a saved layer. A rebuild reuses layers until the first changed one.
- **Rarely changing things at the top, often changing things at the bottom.** Requirements first, code last, so editing code doesn't reinstall pandas.

### .dockerignore
- Like `.gitignore`, but for what Docker copies: `.venv/`, `.git/`, `__pycache__/`, `.pytest_cache/`.
- Without it, the build context was **171 MB** (my venv). Check with `cat -A .dockerignore` that it's actually saved.

### Compose now uses my image
- `image: python:3.12-slim` → `build: .`; `command` → just `pytest -q`.
- Keep the `.:/app` bind mount: the image's code copy is frozen at build time; the mount shows live edits.
- New package in `requirements.txt` → rebuild the image.

### Makefile
- Shortcuts: `make build`, `make run`, `make test`.
- Command lines under a target must start with a **Tab**, or I get `missing separator`.
- `.PHONY` = these are command names, not files, so always run them.

---

## Step 10 · pytest flags and error paths

### Flags
- `-v`: verbose, lists every test by name with PASSED/FAILED.
- `-x`: stop at the first failure.
- `-k engine`: run only tests whose name contains "engine".
- `--lf`: rerun only the tests that failed last time.
- `-q`: quiet, short output.

### Error-path tests
- Bad input should **fail loudly** at the top of the function: `raise ValueError(...)` with a clear message.
- `with pytest.raises(ValueError, match="close"):` — the code inside must raise that error, and the message must contain the text.
- `pytest.raises` only catches the error type I name; a typo (`NameError`) still fails the test.
- **Prove a test can fail:** break the code on purpose. Replace `raise` with `pass` (commenting out only `raise` leaves an empty `if` → `IndentationError`).

---

## Step 11 · Fixtures

- A **fixture** = reusable setup. A test gets it by naming it as a parameter.
- `tests/conftest.py`: fixtures there are available to every test file, no import needed.
- `tmp_path`: built-in fixture giving a fresh empty folder; pytest creates it, I never `mkdir` it.
- Fixtures can use other fixtures (`prices_csv(tmp_path, prices)`); within one test, they all share the same `tmp_path`.
- `return` = hand over a value and finish. `yield` = hand over, let the test run, then run the teardown code after it (even if the test fails).
- Each test gets a **fresh copy** of a fixture, so editing it in one test doesn't affect others.
- A fixture can be requested just for its side effect (`prices_csv` writes the file even if the test never uses the variable).
- `df.drop(columns="close")` returns a new DataFrame without that column.
- Relative paths are looked up from the **current folder**. Always run pytest, make and compose from the repo root.

---

## Step 12 · Parametrize and mocking

### Parametrize
- `@pytest.mark.parametrize("a, b", [(1, 2), (3, 4)], ids=["x", "y"])` runs one test once per case.
- `ids` name the runs in the output (`test_name[x]`).
- Fixtures and parametrized values mix freely; fixtures don't go in the names string.

### Refactor for testing
- Code at the top level of a file runs as soon as it's imported. Wrap it in `def main(argv=None):`.
- `parser.parse_args(argv)`: a test passes a fake list; `None` falls back to the real terminal input.
- `if __name__ == "__main__": main()` → only runs when the file is run directly, not when imported. `"__main__"` needs quotes.

### Mocking
- `monkeypatch.setattr(module, "name", fake)` swaps something for one test, then restores it.
- **Patch where it's used:** `from x import f` copies `f` into the importing module, so patch `backtester.__main__`, not `backtester.data`.
- `lambda path: prices` = a one-line function that ignores its input and returns the fixture.
- `capsys.readouterr()` after the call; `captured.out` is a string (no brackets). Check with `"Trades" in captured.out`.

---

## Step 13 · Look-ahead guard
- Plant an obviously fake close (1.2000) on the signal bar. If the engine wrongly entered at the signal bar's close, the entry would be 1.2000.
- Assert the entry equals the **next bar's open** and does **not** equal 1.2000.

---

## Mistakes I made (watch for these)
- **Quotes vs no quotes:** quotes = literal text, no quotes = a variable (`"/tmp_path"`, `tmp_path / prices`, `__name__ == __main__`).
- **Every name in a function must be a parameter, created earlier in it, or imported** (`csv_path` vs `csv_file`, `equity_last` undefined).
- Calling a method on the wrong object: `path.to_csv` → `prices.to_csv`; `equity.total_return` → `total_return(equity)`.
- A test calling itself instead of the code under test.
- Hard-coding numbers instead of using parameters (`rolling(9)` instead of `rolling(fast)`).
- `x in y` direction: the thing I'm looking for goes on the left.
- `import ... .py`: imports use module names, no `.py`.
- File in the wrong place or misspelled (`metric.py`, a nested `backtest/` folder).
- Unsaved files (dot on the VS Code tab); check what's on disk with `cat -A`.
- Running from the wrong folder (`tests/` instead of the repo root).
- Wrong YAML key names, missing `- ` on list items, missing top-level `volumes:`, laptop path where a container path goes.
- Called `gethostbyname()` without the hostname argument.