load_prices(path) takes a CSV path and returns a DataFrame sorted by time. It fails loudly if a column is missing.


total_return(equity) and max_drawdown(equity) each take a Series of account values and return a single number.

## Step 7.1 · Compose drill
- In Compose, services reach each other by name: `app` found `db` just by calling it "db" (no IPs needed).
- `docker compose down` removes containers but keeps named volumes (data survives); `down -v` deletes the volumes too.
- `depends_on` only waits for a container to start, not to be ready (use a healthcheck for that).



## Step 7 · Docker Compose — what I learnt

### Terminal vs YAML
- `docker ...` / `docker compose ...` commands run in the **terminal** (docker is just another program, like git).
- `docker-compose.yml` is a **description**, not commands. Compose reads it and runs Docker for me.
- The YAML is like a long `docker run` saved in a file:
  `image` = image name · `volumes` = `-v` · `environment` = `-e` · `ports` = `-p` · `working_dir` = `-w` · `command` = the command at the end.

### YAML rules
- Indentation shows what belongs to what. **Spaces only, never tabs**, and be consistent.
- `key: value` = one setting. A line starting with `- ` = one item in a **list**.
- Lists needed for: `volumes`, `depends_on`.
- Key names must be exact: `command` (not commands), `depends_on` (not depends), `working_dir` (not working_dr).

### Key ideas
- **Services reach each other by name.** In the drill, `app` found `db` just by calling it "db".
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

### Dockerfile
- Not needed yet: step 7 uses ready-made images (`image:`).
- Downside: `pip install` runs on every test run. Step 9's Dockerfile bakes packages into my own image once, then Compose uses `build: .` instead of `image:`.

### Mistakes I made (watch for these)
- Wrong key names: `depends`, `commands`, `working_dr`.
- Forgot the `- ` on list items.
- Forgot the top-level `volumes:` for a named volume.
- Put my laptop path where a container path goes.
- Called `gethostbyname()` without the hostname argument.



