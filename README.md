# StealthPlex

**Python web scraping when basic HTTP gets blocked** — Cloudflare (Turnstile, interstitial), Akamai, Imperva, Datadome, and similar bot walls.

StealthPlex is a thin layer over the tools you’d reach for anyway: [curl_cffi](https://github.com/lexiforest/curl_cffi) and [wreq](https://github.com/0x676e67/wreq-python) for **TLS / JA3-style fingerprints**, [cloudscraper](https://github.com/VeNoMouS/cloudscraper) for **Cloudflare cookie sessions**, [Scrapling](https://github.com/D4Vinci/Scrapling) for **stealth headless fetch**, and [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) **UC + CDP mode** when you need a real browser that doesn’t trip the easy checks. Pick one engine up front, or turn on **fallback** and let it step up from fast HTTP → bypass → stealth → CDP automation.

```python
from StealthPlex import Fetch

fetch = Fetch(engine="curl_cffi")          # TLS impersonation, HTTP/2/3
fetch = Fetch(engine="cloudscraper")       # Cloudflare-aware session
fetch = Fetch(engine="seleniumbase")       # UC + CDP (not plain Driver)
fetch = Fetch(fallback=True)               # try the chain; get .engine + .attempts
```

Each `Fetch(engine=...)` handle is the **real upstream API** (types, autocomplete, docs)—not a dumbed-down wrapper. Good for scrapers, price monitors, research crawlers, and any job where you’re tired of rewriting the stack every time a site adds protection.

**Fallback order (default):** wreq → curl_cffi → cloudscraper → scrapling → seleniumbase

## Install

Requires [uv](https://docs.astral.sh/uv/).

```bash
# Core only (no engines)
uv sync

# One engine
uv sync --extra curl_cffi
uv sync --extra wreq
uv sync --extra cloudscraper
uv sync --extra scrapling
uv sync --extra seleniumbase

# All engines
uv sync --extra all
```

## Engines

| Engine | Extra | Upstream | Detailed Docs |
|--------|-------|----------|---------------|
| `wreq` | `wreq` | [0x676e67/wreq-python](https://github.com/0x676e67/wreq-python) | [wreq Guide](StealthPlex/engines/wreq/README.md) |
| `curl_cffi` | `curl_cffi` | [lexiforest/curl_cffi](https://github.com/lexiforest/curl_cffi) | [curl_cffi Guide](StealthPlex/engines/curl_cffi/README.md) |
| `cloudscraper` | `cloudscraper` | [VeNoMouS/cloudscraper](https://github.com/VeNoMouS/cloudscraper) | [cloudscraper Guide](StealthPlex/engines/cloudscraper/README.md) |
| `scrapling` | `scrapling` | [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) | [scrapling Guide](StealthPlex/engines/scrapling/README.md) |
| `seleniumbase` | `seleniumbase` | [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase) | [seleniumbase Guide](StealthPlex/engines/seleniumbase/README.md) |

Hover the `fetch` variable in your IDE (after assigning it via `Fetch()`) to view engine-specific autocomplete documentation and links.

---

## Quick Start

You can bind directly to a specific engine to access its full upstream API, or use the multi-engine fallback client.

### 1. Engine-Specific Examples

#### wreq (TLS Impersonation - Async)
```python
import asyncio
from StealthPlex import Fetch

async def main():
    fetch = Fetch(engine="wreq")
    response = await fetch.get("https://example.com", emulation=fetch.Emulation.Firefox149)
    print(await response.text())

asyncio.run(main())
```

#### curl_cffi (TLS Impersonation - Sync/Async)
```python
from StealthPlex import Fetch

fetch = Fetch(engine="curl_cffi")
response = fetch.get("https://example.com", impersonate="chrome124")
print(response.text)
```

#### cloudscraper (Cloudflare Session Bypass)
```python
from StealthPlex import Fetch

fetch = Fetch(engine="cloudscraper")
scraper = fetch.create_scraper(browser="chrome")
response = scraper.get("https://example.com")
print(response.text)
```

#### scrapling (Stealth Headless Fetch & Selector)
```python
from StealthPlex import Fetch

fetch = Fetch(engine="scrapling")
response = fetch.fetcher.fetch("https://example.com")
print(response.text)
```

#### seleniumbase (Hard-Target Browser UC/CDP Automation)
```python
from StealthPlex import Fetch

fetch = Fetch(engine="seleniumbase")
with fetch.SB(uc=True) as sb:
    sb.activate_cdp_mode("https://example.com")
    sb.sleep(2.0)
    print(sb.get_page_source())
```

### 2. Multi-Engine Fallback (Auto-escalation)

```python
from StealthPlex import Fetch

# Fallback walks a chain: wreq -> curl_cffi -> cloudscraper -> scrapling -> seleniumbase
# Returns a normalized StealthPlex Response
fetch = Fetch(fallback=True)
response = fetch.get("https://example.com")
print(f"Bypassed using engine: {response.engine} in {len(response.attempts)} attempt(s)")
print(response.status_code)
```

---

## API Summary

| Need | Use | Detailed Integration Docs |
|------|-----|---------------------------|
| Full [wreq](https://github.com/0x676e67/wreq-python) API (async + blocking) | `Fetch(engine="wreq")` | [wreq Guide](StealthPlex/engines/wreq/README.md) |
| Full [curl_cffi](https://github.com/lexiforest/curl_cffi) API (sync + async) | `Fetch(engine="curl_cffi")` | [curl_cffi Guide](StealthPlex/engines/curl_cffi/README.md) |
| Full [cloudscraper](https://github.com/VeNoMouS/cloudscraper) API | `Fetch(engine="cloudscraper")` | [cloudscraper Guide](StealthPlex/engines/cloudscraper/README.md) |
| Adaptive fetch + crawl ([Scrapling](https://github.com/D4Vinci/Scrapling)) | `Fetch(engine="scrapling")` | [scrapling Guide](StealthPlex/engines/scrapling/README.md) |
| Full [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) API | `Fetch(engine="seleniumbase")` | [seleniumbase Guide](StealthPlex/engines/seleniumbase/README.md) |
| Try next engine when blocked | `Fetch(fallback=True)` | |
| Shortcut methods | `curl_fetch()`, `wreq_fetch()`, `cloudscraper_fetch()`, `scrapling_fetch()`, `seleniumbase_fetch()` | |

