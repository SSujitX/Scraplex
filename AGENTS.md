# StealthPlex — agent rules

## Naming (banned words)

| Banned | Use instead |
|--------|-------------|
| `backend`, `Backend`, `backends/` | **engine** concept; implementations in `StealthPlex/engines/` |
| `policy`, `Policy` | `engine=` or `fallback=` |
| `open_backend`, `open_engine`, `Use` | **`Fetch`** |
| `Client` as factory | **`Fetch(engine=...)`** — `Client` only as upstream wreq type |
| `Engine` as factory callable | **`Fetch(engine=...)`** — `Engine` Protocol in `engines/base.py` only |

## Tooling

- **uv only** (`uv sync`, `uv add`, `uv run`, `uv lock`)
- Python `>=3.11`; manual check `uv run test_*.py` (no pytest/ruff)
- Extras: `uv sync --extra wreq|curl_cffi|cloudscraper|scrapling|seleniumbase|all`

## Libraries

| Engine | PyPI | Extra | Layer | GitHub |
|--------|------|-------|-------|--------|
| wreq | `wreq` | `wreq` | L1 | https://github.com/0x676e67/wreq-python |
| curl_cffi | `curl-cffi` | `curl_cffi` | L1 | https://github.com/lexiforest/curl_cffi |
| cloudscraper | `cloudscraper` | `cloudscraper` | L2 | https://github.com/VeNoMouS/cloudscraper |
| scrapling | `scrapling` | `scrapling` | L3 | https://github.com/D4Vinci/Scrapling |
| seleniumbase | `seleniumbase` | `seleniumbase` | L4 | https://github.com/seleniumbase/SeleniumBase |

- Core install has no engines; `Fetch(engine=...)` needs the matching extra
- `DEFAULT_FALLBACK`: L1→L4 order above (installed only)

## User API (two paths only)

```python
from StealthPlex import Fetch

# Bound engine: full upstream API on the fetch handle
fetch = Fetch(engine="curl_cffi")
fetch.get(url, impersonate="chrome")       # curl_cffi.get
s = fetch.Session()                        # curl_cffi.Session()
ws = fetch.WebSocket(...)                  # curl_cffi.WebSocket

fetch = Fetch(engine="wreq")
await fetch.get(url, emulation=fetch.Emulation.Firefox149)

fetch = Fetch(engine="cloudscraper")
scraper = fetch.create_scraper(browser="chrome")
scraper.get(url)

# Multi-engine: StealthPlex Response + fallback chain
fetch = Fetch(fallback=True)
resp = fetch.get(url)                  # StealthPlex.response.Response
```

| Need | Use |
|------|-----|
| curl_cffi 1:1 + IDE hints | `Fetch(engine="curl_cffi")` — full package via `__getattr__` |
| wreq 1:1 + IDE hints | `Fetch(engine="wreq")` |
| cloudscraper 1:1 + IDE hints | `Fetch(engine="cloudscraper")` |
| seleniumbase 1:1 + IDE hints | `Fetch(engine="seleniumbase")` |
| Try next engine when blocked | `Fetch(fallback=True)` → StealthPlex `Response` |

## Engine handles

| Engine | Handle | Call |
|--------|--------|------|
| wreq | module proxy | `await fetch.get(...)`, `fetch.Client(...)`, `fetch.blocking.Client` |
| curl_cffi | module proxy | `fetch.get`, `fetch.aio.get`, `fetch.Session`, `fetch.AsyncSession` |
| cloudscraper | module proxy | `fetch.create_scraper().get(...)`, `fetch.get_tokens(url)` |
| scrapling | `.fetcher` | `fetch.fetcher.fetch(..., headless=)` |
| seleniumbase | module proxy | `with fetch.SB(uc=True) as sb: sb.activate_cdp_mode(url)`, `sb.cdp.*`, `fetch.sb_cdp` |

- IDE: per-engine `proxy.pyi`; runtime `apply_fetch_doc()` for hover on assigned `fetch`
- `Fetch(engine=...)` and `Fetch(fallback=...)` mutually exclusive
- `fallback=True`: `DEFAULT_FALLBACK`, skip uninstalled
- Never auto `pip install` extras

## Layout (no `src/` — package at repo root)

```
StealthPlex/                         # repo root
  StealthPlex/                       # import StealthPlex (capital S and P)
    factory.py / factory.pyi      # Fetch()
    fallback_client.py          # FallbackClient
    engines/
      curl_cffi/                  # proxy.py, proxy.pyi, engine.py, _docs.py
      wreq/
      cloudscraper/
      seleniumbase/
  test_curl_cffi.py
  test_wreq.py
```

- `import StealthPlex` not `stealthplex` (Windows: never delete `stealthplex` folder — same path as `StealthPlex`)
- Hatch: `packages = ["StealthPlex"]`; stubs `*.pyi` included

## Implementation

- `Fetch()` in `factory.py` with `@overload` per `EngineId`
- `Engine` Protocol in `engines/base.py`; `*Engine` in `engines/*/engine.py`
- `Response`: `status_code`, `headers`, `content`, `text`, `url`, `cookies`, `engine`, `attempts`, `handle`
- Upstream kwargs via handle only

## Git commits

- Use conventional prefixes: `feat:`, `fix:`, `docs:`, `test:`, `chore:`, etc.
- **Never** add `Co-authored-by: Cursor <cursoragent@cursor.com>` (or any Cursor co-author trailer) to commit messages.
- Do not add other agent/tool co-author lines unless the user explicitly requests them.

## Code style

- One-line docstrings; full `ANN`; max line 100

## Commands

```bash
uv sync --extra curl_cffi && uv run test_curl_cffi.py
uv sync --extra wreq && uv run test_wreq.py
uv sync --extra cloudscraper && uv run test_cloudscraper.py
uv sync --extra scrapling && uv run test_scrapling.py
uv sync --extra seleniumbase && uv run test_seleniumbase.py
uv lock --upgrade
```
