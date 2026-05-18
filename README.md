# Scraplex

Scraplex is a multi-engine fetch layer for Python scraping. You choose how hard a target is to reach—then bind the right tool without rewriting your project.

Use **one engine** when you know what works: TLS impersonation with [curl_cffi](https://github.com/lexiforest/curl_cffi), async fingerprinting with [wreq](https://github.com/0x676e67/wreq-python), Cloudflare sessions with [cloudscraper](https://github.com/VeNoMouS/cloudscraper), adaptive crawls with [Scrapling](https://github.com/D4Vinci/Scrapling), or full browser control with [SeleniumBase](https://github.com/seleniumbase/SeleniumBase). Each path exposes that library’s real API on a single `fetch` handle—autocomplete, docstrings, and upstream types included.

Use **fallback** when you do not: Scraplex walks a chain (fast HTTP → bypass → stealth → browser) and returns one normalized `Response` with `.engine` and `.attempts` so you can see what finally worked.

One import (`Fetch`), several strategies, zero wrapper lock-in.

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

| Engine | Extra | Docs |
|--------|-------|------|
| [curl_cffi](https://github.com/lexiforest/curl_cffi) | `curl_cffi` | TLS/JA3 impersonation, HTTP/2/3 — sync + async |
| [wreq](https://github.com/0x676e67/wreq-python) | `wreq` | Async HTTP + TLS fingerprint |
| [cloudscraper](https://github.com/VeNoMouS/cloudscraper) | `cloudscraper` | Cloudflare bypass (Requests session) |
| [Scrapling](https://github.com/D4Vinci/Scrapling) | `scrapling` | Adaptive parsers, stealth fetch, spiders (planned) |
| [seleniumbase](https://github.com/seleniumbase/SeleniumBase) | `seleniumbase` | Browser automation (planned) |

Hover the `fetch` variable after `Fetch(engine="...")` for engine-specific docs and the upstream GitHub link.

---

## curl_cffi

Upstream: [lexiforest/curl_cffi](https://github.com/lexiforest/curl_cffi)

```bash
uv sync --extra curl_cffi
```

```python
import asyncio

from Scraplex import Fetch

fetch = Fetch(engine="curl_cffi")

# Sync — module-level shortcut (like curl_cffi.get)
response = fetch.get("https://tls.browserleaks.com/json", impersonate="chrome")
print(response.status_code)
print(response.json())

# Sync — persistent session (like curl_cffi.Session)
session = fetch.Session(impersonate="chrome124")
session.get("https://httpbin.org/cookies/set/foo/bar")
print(session.cookies)

# Async — one-shot (fetch.aio.*)
async def aio_shortcut():
    r = await fetch.aio.get("https://httpbin.org/get", impersonate="chrome")
    print(r.status_code, r.json())

# Async — persistent session (like curl_cffi.AsyncSession)
async def aio_session():
    async with fetch.AsyncSession(impersonate="chrome124") as session:
        r = await session.get("https://httpbin.org/get")
        print(r.status_code, r.json()["url"])

asyncio.run(aio_shortcut())
asyncio.run(aio_session())
```

Also on `fetch`: `post`, `put`, `patch`, `delete`, `head`, `options`, `trace`, `query`, `request`, `WebSocket`, `AsyncWebSocket`, and everything in `curl_cffi.__all__`.

```bash
uv run test_curl_cffi.py
uv run test_curl_cffi_async.py
```

---

## wreq

Upstream: [0x676e67/wreq-python](https://github.com/0x676e67/wreq-python)

```bash
uv sync --extra wreq
```

```python
import asyncio

from Scraplex import Fetch

fetch = Fetch(engine="wreq")

# Async — module-level shortcut (like wreq.get)
async def main():
    r = await fetch.get("https://httpbin.org/get", emulation=fetch.Emulation.Firefox149)
    print(r.status)
    print(await r.text())

# Async — persistent client (like wreq.Client)
async def with_client():
    wc = fetch.Client(emulation=fetch.Emulation.Firefox149)
    r = await wc.get("https://httpbin.org/get")
    print(await r.text())
    wc.close()

# Sync — blocking client (like wreq.blocking.Client)
def blocking_example():
    bc = fetch.blocking.Client(emulation=fetch.Emulation.Firefox149)
    r = bc.get("https://httpbin.org/get")
    print(r.text())
    bc.close()

asyncio.run(main())
```

Also on `fetch`: `post`, `put`, `patch`, `delete`, `head`, `options`, `trace`, `request`, `websocket`, `Emulation`, `Proxy`, and everything in `wreq.__all__`.

```bash
uv run test_wreq.py
```

---

## cloudscraper

Upstream: [VeNoMouS/cloudscraper](https://github.com/VeNoMouS/cloudscraper)

```bash
uv sync --extra cloudscraper
```

```python
from Scraplex import Fetch

fetch = Fetch(engine="cloudscraper")

# Session — like cloudscraper.create_scraper()
scraper = fetch.create_scraper(browser="chrome")
r = scraper.get("https://example.com")
print(r.status_code, r.text)

# Or instantiate directly
scraper = fetch.CloudScraper(interpreter="native")
r = scraper.post("https://httpbin.org/post", json={"ok": True})

# Integration helpers (module-level)
tokens, user_agent = fetch.get_tokens("https://example.com")
cookie_header, user_agent = fetch.get_cookie_string("https://example.com")
```

Also on `fetch`: `session`, `CipherSuiteAdapter`, `Cloudflare`, `exceptions`, `captcha`, `interpreters`, `user_agent`, and the rest of the `cloudscraper` module.

```bash
uv run test_cloudscraper.py
```

---

## scrapling *(coming soon)*

Upstream: [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling)

[Scrapling](https://github.com/D4Vinci/Scrapling) is an adaptive web scraping framework built for sites that change and defenses that escalate. Its parser relocates selectors when layouts shift. Its fetchers target anti-bot surfaces—including Cloudflare Turnstile—without bolting on a second stack. Its spider layer scales from one-off requests to concurrent, multi-session crawls with pause/resume and rotating proxies, still in a few lines of Python.

In Scraplex, Scrapling is the **stealth / crawl** tier: you keep its full API on `fetch` (fetchers, parsers, spiders) while lighter engines handle TLS-only or session-only work elsewhere in the same project.

```bash
uv sync --extra scrapling   # when the engine is wired in
```

```python
from Scraplex import Fetch

fetch = Fetch(engine="scrapling")

# Single stealth fetch (headless or dynamic)
page = fetch.fetcher.fetch("https://example.com", headless=True)

# Scale up: parsers, spiders, sessions — same fetch handle, upstream Scrapling API
# spider = fetch.Spider(...)
# spider.crawl(...)
```

---

## seleniumbase *(coming soon)*

Upstream: [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)

SeleniumBase is the **hard-target / full browser** tier: real browser sessions for CAPTCHAs, heavy JavaScript, and flows the HTTP engines cannot drive. Scraplex exposes `fetch.sb` and the rest of the SeleniumBase API when this engine is enabled.

```python
fetch = Fetch(engine="seleniumbase")
with fetch.sb as sb:
    sb.open("https://example.com")
```

---

## Multi-engine fallback (optional)

Returns a Scraplex `Response` (not the upstream library type). Tries engines in order: wreq → curl_cffi → cloudscraper → scrapling → seleniumbase.

```python
from Scraplex import Fetch

fetch = Fetch(fallback=True)
r = fetch.get("https://example.com")
print(r.engine, r.attempts, r.status_code)
```

---

## API summary

| Need | Use |
|------|-----|
| Full [curl_cffi](https://github.com/lexiforest/curl_cffi) API (sync + async) | `Fetch(engine="curl_cffi")` |
| Full [wreq](https://github.com/0x676e67/wreq-python) API (async + blocking) | `Fetch(engine="wreq")` |
| Full [cloudscraper](https://github.com/VeNoMouS/cloudscraper) API | `Fetch(engine="cloudscraper")` |
| Adaptive fetch + crawl ([Scrapling](https://github.com/D4Vinci/Scrapling)) | `Fetch(engine="scrapling")` *(planned)* |
| Browser automation ([SeleniumBase](https://github.com/seleniumbase/SeleniumBase)) | `Fetch(engine="seleniumbase")` *(planned)* |
| Try next engine when blocked | `Fetch(fallback=True)` |
| Shortcuts | `curl_fetch()`, `wreq_fetch()`, `cloudscraper_fetch()` |
