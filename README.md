# StealthPlex

**Stealth web scraping when basic HTTP gets blocked** — Cloudflare (Turnstile, interstitial), Akamai, Imperva, Datadome, and similar bot walls.

StealthPlex wraps the tools you'd reach for anyway — [wreq](https://github.com/0x676e67/wreq-python), [curl_cffi](https://github.com/lexiforest/curl_cffi), [cloudscraper](https://github.com/VeNoMouS/cloudscraper), [Scrapling](https://github.com/D4Vinci/Scrapling), and [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) — behind a single `Fetch()` interface with **built-in stealth**: randomized browser fingerprints (User-Agent, Sec-CH-UA, Sec-Fetch-*, Accept-Language, Referer), automatic TLS/JA3 impersonation, and serial engine escalation from fast HTTP all the way to stealth browser UC/CDP automation (headed on Windows/macOS, auto-Xvfb on Linux).

```python
from StealthPlex import Fetch

# Zero config — stealth headers + serial engine fallback
fetch = Fetch()
resp = fetch.get("https://protected-site.com")
print(resp.text)      # HTML
print(resp.json())    # or JSON
print(resp.engine)    # which engine bypassed
```

**Fallback chain:** wreq → curl_cffi → cloudscraper → scrapling → seleniumbase  
Each request gets **randomized stealth fingerprints**. If one engine gets blocked, the next one takes over automatically.

## Install

### 1. Installation

StealthPlex core has no default engine dependencies to remain lightweight. You must install at least one engine extra to perform requests:

```bash
# Install with all engines (recommended for maximum fallback capability)
uv add StealthPlex --extra all
# or
pip install "StealthPlex[all]"

# Install specific engines only (e.g. curl_cffi and seleniumbase)
uv add StealthPlex --extra curl_cffi --extra seleniumbase
# or
pip install "StealthPlex[curl_cffi,seleniumbase]"
```

### 2. Upgrading Engines (Bypass Updates)

Because anti-bot protections change constantly, you should keep all engine packages updated to their latest versions:

```bash
# Using uv (automatically upgrades all optional engines)
uv add --upgrade "StealthPlex[all]"

# Using pip (requires --upgrade-strategy eager to force upgrade of all extra engines)
pip install --upgrade --upgrade-strategy eager "StealthPlex[all]"
```


## Engines

| Engine | Extra | Layer | Upstream | Detailed Docs |
|--------|-------|-------|----------|---------------|
| `wreq` | `wreq` | L1 | [0x676e67/wreq-python](https://github.com/0x676e67/wreq-python) | [wreq Guide](StealthPlex/engines/wreq/README.md) |
| `curl_cffi` | `curl_cffi` | L1 | [lexiforest/curl_cffi](https://github.com/lexiforest/curl_cffi) | [curl_cffi Guide](StealthPlex/engines/curl_cffi/README.md) |
| `cloudscraper` | `cloudscraper` | L2 | [VeNoMouS/cloudscraper](https://github.com/VeNoMouS/cloudscraper) | [cloudscraper Guide](StealthPlex/engines/cloudscraper/README.md) |
| `scrapling` | `scrapling` | L3 | [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) | [scrapling Guide](StealthPlex/engines/scrapling/README.md) |
| `seleniumbase` | `seleniumbase` | L4 | [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase) | [seleniumbase Guide](StealthPlex/engines/seleniumbase/README.md) |

---

## Quick Start — Stealth Fallback (Default)

Just call `Fetch()` — no engine needed. StealthPlex injects stealth headers and walks the engine chain serially until one bypasses.

### Basic GET — Parse HTML or JSON

```python
from StealthPlex import Fetch

fetch = Fetch()

# GET with full stealth headers auto-injected
resp = fetch.get("https://httpbin.org/get")
print(resp.status_code)
print(resp.text)                           # raw HTML/text
print(resp.json())                         # auto-parse JSON
print(resp.engine)                         # "wreq", "curl_cffi", etc.
print(resp.attempts)                       # ("wreq",) or ("wreq", "curl_cffi")
print(resp.ok)                             # True if status < 400
```

### POST with JSON body

```python
from StealthPlex import Fetch

fetch = Fetch()
resp = fetch.post(
    "https://httpbin.org/post",
    json={"username": "admin", "password": "secret"},
    headers={"X-Custom": "value"},
)
print(resp.json())
```

### PUT, DELETE, PATCH, HEAD, OPTIONS

```python
from StealthPlex import Fetch

fetch = Fetch()

# PUT with raw data
resp = fetch.put("https://httpbin.org/put", data="update payload")
print(resp.json())

# DELETE
resp = fetch.delete("https://httpbin.org/delete")
print(resp.status_code)

# PATCH with JSON
resp = fetch.patch("https://httpbin.org/patch", json={"key": "val"})
print(resp.json())

# HEAD (status + headers only)
resp = fetch.head("https://httpbin.org/get")
print(resp.status_code, resp.headers)

# OPTIONS
resp = fetch.options("https://httpbin.org/get")
print(resp.status_code)
```

### Custom Headers, Cookies, Params, Redirects

```python
from StealthPlex import Fetch

fetch = Fetch()

# All parameters work with full IDE autocomplete
resp = fetch.get(
    "https://httpbin.org/get",
    headers={"Authorization": "Bearer token123"},
    cookies={"session": "abc123"},
    params={"q": "stealth scraping", "page": "1"},
    timeout=30.0,
    allow_redirects=False,         # or redirect=False
)
print(resp.status_code)
print(resp.json())
```

### Custom Fallback Order

```python
from StealthPlex import Fetch

# Only try these two engines in this order
fetch = Fetch(fallback=["curl_cffi", "cloudscraper"])
resp = fetch.get("https://example.com")
print(resp.engine)
```

---

## Engine-Specific Examples

For full upstream API access (types, autocomplete, docs), bind to a specific engine:

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

#### scrapling (Stealth Browser Fetch & Selector)
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

---

## API Summary

| Need | Use | Docs |
|------|-----|------|
| **Stealth auto-bypass (recommended)** | **`Fetch()`** | — |
| Custom engine order | `Fetch(fallback=["wreq", "curl_cffi"])` | — |
| Full [wreq](https://github.com/0x676e67/wreq-python) API | `Fetch(engine="wreq")` | [Guide](StealthPlex/engines/wreq/README.md) |
| Full [curl_cffi](https://github.com/lexiforest/curl_cffi) API | `Fetch(engine="curl_cffi")` | [Guide](StealthPlex/engines/curl_cffi/README.md) |
| Full [cloudscraper](https://github.com/VeNoMouS/cloudscraper) API | `Fetch(engine="cloudscraper")` | [Guide](StealthPlex/engines/cloudscraper/README.md) |
| Adaptive fetch ([Scrapling](https://github.com/D4Vinci/Scrapling)) | `Fetch(engine="scrapling")` | [Guide](StealthPlex/engines/scrapling/README.md) |
| Full [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) API | `Fetch(engine="seleniumbase")` | [Guide](StealthPlex/engines/seleniumbase/README.md) |
| Shortcuts | `curl_fetch()`, `wreq_fetch()`, `cloudscraper_fetch()`, `scrapling_fetch()`, `seleniumbase_fetch()` | — |
