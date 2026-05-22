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

| Engine | Extra | Docs |
|--------|-------|------|
| [curl_cffi](https://github.com/lexiforest/curl_cffi) | `curl_cffi` | TLS/JA3 impersonation, HTTP/2/3 — sync + async |
| [wreq](https://github.com/0x676e67/wreq-python) | `wreq` | Async HTTP + TLS fingerprint |
| [cloudscraper](https://github.com/VeNoMouS/cloudscraper) | `cloudscraper` | Cloudflare bypass (Requests session) |
| [Scrapling](https://github.com/D4Vinci/Scrapling) | `scrapling` | Adaptive parsers, stealth fetch, spiders (planned) |
| [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) | `seleniumbase` | UC Mode + CDP Mode (stealth; not plain Driver) |

Hover the `fetch` variable after `Fetch(engine="...")` for engine-specific docs and the upstream GitHub link.

---

## curl_cffi

Upstream: [lexiforest/curl_cffi](https://github.com/lexiforest/curl_cffi)

```bash
uv sync --extra curl_cffi
```

```python
import asyncio

from StealthPlex import Fetch

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

from StealthPlex import Fetch

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
from StealthPlex import Fetch

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

## scrapling

Upstream: [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling)

[Scrapling](https://github.com/D4Vinci/Scrapling) is an adaptive web scraping framework built for sites that change and defenses that escalate. Its parser relocates selectors when layouts shift. Its fetchers target anti-bot surfaces—including Cloudflare Turnstile—without bolting on a second stack. Its spider layer scales from one-off requests to concurrent, multi-session crawls with pause/resume and rotating proxies, still in a few lines of Python.

In StealthPlex, Scrapling is the **stealth / crawl** tier (bound to engine identifier `"scrapling"`): you keep its full API on `fetch` (fetchers, parsers, spiders) while lighter engines handle TLS-only or session-only work elsewhere in the same project.

```bash
uv sync --extra scrapling
```

> [!NOTE]
> Browser binaries and setup are automatically configured on first run if missing.


```python
import asyncio
from StealthPlex import Fetch

fetch = Fetch(engine="scrapling")

# 1. 100% Stealth Fetch (Sync)
# Bypass Cloudflare Turnstile, prevent WebRTC/DNS leaks, and randomize fingerprints
resp = fetch.StealthyFetcher.fetch(
    "https://nowsecure.nl",  # Cloudflare-protected target
    solve_cloudflare=True,   # Solve Turnstile/Interstitial challenges automatically
    block_webrtc=True,       # Prevent local/real IP leaks via WebRTC when using proxies
    hide_canvas=True,        # Add random noise to canvas operations to avoid fingerprinting
    dns_over_https=True,     # Route DNS queries via DoH to prevent DNS leaks
    block_ads=True,          # Block tracking script requests to speed up loading
    google_search=True,      # Spoof a Google search referer header (default is True)
    headless=True,           # Run in stealthy headless chromium mode
    proxy="http://username:password@host:port"  # Proxy setting (optional)
)
print(f"Status: {resp.status}")
print(f"IP: {resp.xpath('//body').get()[:200]}")  # Uses Scrapling's Selector engine automatically


# 2. 100% Stealth Fetch (Async)
async def stealth_fetch_async():
    resp = await fetch.StealthyFetcher.async_fetch(
        "https://nowsecure.nl",
        solve_cloudflare=True,
        block_webrtc=True,
        hide_canvas=True,
        dns_over_https=True,
        headless=True,
        proxy="http://username:password@host:port"
    )
    print(f"Async Status: {resp.status}")

asyncio.run(stealth_fetch_async())


# 3. Persistent Stealth Session (Sync)
# Reuse browser context, cookies, and fingerprint headers across multiple requests
with fetch.StealthySession(
    solve_cloudflare=True,
    block_webrtc=True,
    hide_canvas=True,
    dns_over_https=True,
    proxy="http://username:password@host:port"
) as session:
    # First request solves Cloudflare and saves cookies
    resp1 = session.get("https://nowsecure.nl")
    print(f"Session Page 1: {resp1.status}")
    
    # Second request reuses the authenticated session context
    resp2 = session.get("https://nowsecure.nl/another-page")
    print(f"Session Page 2: {resp2.status}")


# 4. Persistent Stealth Session (Async)
async def session_crawl_async():
    async with fetch.AsyncStealthySession(
        solve_cloudflare=True,
        block_webrtc=True,
        hide_canvas=True,
        dns_over_https=True,
        proxy="http://username:password@host:port"
    ) as session:
        resp1 = await session.get("https://nowsecure.nl")
        print(f"Async Session Page 1: {resp1.status}")
        
        resp2 = await session.get("https://nowsecure.nl/another-page")
        print(f"Async Session Page 2: {resp2.status}")

asyncio.run(session_crawl_async())


# 5. Spiders Crawling Framework
# Scale to large concurrent spider jobs with spider architecture
class StealthSpider(fetch.spiders.Spider):
    name = "stealth_spider"
    start_urls = ["https://httpbin.org/html"]

    def parse(self, response):
        print(response.xpath("//h1/text()").get())

spider = StealthSpider()
spider.start()
```

Also on `fetch`: `Fetcher`, `StealthyFetcher`, `DynamicFetcher`, `AsyncFetcher`, `Selector`, `spiders`, `fetchers`, `parser`, `FetcherSession`, `StealthySession`, `DynamicSession`, `AsyncStealthySession`, `AsyncDynamicSession`.

```bash
uv run test_scrapling.py
```

---

## seleniumbase

Upstream: [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase) · CDP docs: [examples/cdp_mode](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/ReadMe.md)

```bash
uv sync --extra seleniumbase
```

[SeleniumBase](https://github.com/seleniumbase/SeleniumBase) is the **hard-target / full browser** tier. For anti-bot sites, use **UC Mode + CDP Mode** — not a plain `Driver()` session. `activate_cdp_mode()` disconnects WebDriver and routes actions through the Chrome DevTools Protocol (`sb.cdp.*`), which is what bypasses Cloudflare, CAPTCHAs, and similar protections.

StealthPlex exposes the full package on `fetch`: `SB`, `sb_cdp`, `cdp_driver`, `BaseCase`, and the rest of `import seleniumbase`.

### UC Mode + CDP Mode (With CDP)

This is the standard stealth context manager flow (With CDP). `activate_cdp_mode()` disconnects WebDriver and routes actions through the Chrome DevTools Protocol (`sb.cdp.*`), allowing you to bypass Cloudflare Turnstile, CAPTCHAs, etc.

```python
from StealthPlex import Fetch

fetch = Fetch(engine="seleniumbase")

with fetch.SB(uc=True, test=True) as sb:
    # Navigate to a Cloudflare Turnstile protected page
    url = "https://seleniumbase.io/apps/turnstile"
    sb.activate_cdp_mode(url)
    sb.sleep(2.0)

    # Solve the challenge using CDP mode
    sb.solve_captcha()
    sb.sleep(2.0)

    # Interact with stealthy CDP methods on sb.cdp
    if sb.cdp.is_element_visible("img#captcha-success"):
        print("Success! Bypassed Cloudflare with context manager.")
```

Common CDP calls on the session (after `activate_cdp_mode`):

```python
sb.cdp.click(selector)
sb.cdp.click_if_visible(selector)
sb.cdp.solve_captcha()
sb.cdp.type(selector, text)
sb.cdp.gui_click_element(selector)   # PyAutoGUI when CDP is not enough
sb.get_page_source()                 # works while WebDriver is disconnected
sb.reconnect()                       # back to WebDriver (may be detectable)
sb.is_connected()
```

### Pure CDP Mode (Raw CDP Sync)

Uses a pure Chrome DevTools Protocol session directly without any WebDriver overhead or process initialization wrapper.

```python
from StealthPlex import Fetch

fetch = Fetch(engine="seleniumbase")

# Initialize sync browser in Pure CDP mode (no WebDriver)
sb = fetch.sb_cdp.Chrome("https://seleniumbase.io/apps/turnstile")
try:
    sb.sleep(2.0)

    # Solve the Turnstile challenge
    sb.solve_captcha()
    sb.sleep(2.0)

    if sb.is_element_visible("img#captcha-success"):
        print("Success! Bypassed Cloudflare in Raw CDP Sync mode.")
finally:
    # Always stop the driver to clean up the browser process
    sb.driver.stop()
```

### Async Pure CDP Mode (Raw CDP Async)

You can also run Pure CDP mode asynchronously using `cdp_driver.start_async()`.

```python
import asyncio
from StealthPlex import Fetch

async def main():
    fetch = Fetch(engine="seleniumbase")

    # Start the async CDP driver
    driver = await fetch.cdp_driver.start_async(headless=False)
    try:
        tab = driver.page
        await tab.get("https://seleniumbase.io/apps/turnstile")
        await tab.sleep(2.0)

        # Solve Cloudflare Turnstile asynchronously
        await tab.solve_captcha()
        await tab.sleep(2.0)

        if await tab.is_element_visible("img#captcha-success"):
            print("Success! Bypassed Cloudflare in Raw CDP Async mode.")
    finally:
        # Stop the driver (synchronous method)
        driver.stop()

asyncio.run(main())
```

### What not to use for protected sites

Plain `fetch.Driver()` / `driver.get()` is standard Selenium WebDriver — fine for normal sites, **not** the stealth/CDP path SeleniumBase documents for anti-bot bypass. Prefer `SB(uc=True)` + `activate_cdp_mode()`.

Also on `fetch`: `cdp_driver` (async CDP), `decorators`, `page_actions`, `fixtures`, `BaseCase`, and everything in `seleniumbase`.

```bash
uv run test_seleniumbase.py
```


---

## Multi-engine fallback (optional)

Returns a StealthPlex `Response` (not the upstream library type). Tries engines in order: wreq → curl_cffi → cloudscraper → scrapling → seleniumbase.

```python
from StealthPlex import Fetch

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
| Adaptive fetch + crawl ([Scrapling](https://github.com/D4Vinci/Scrapling)) | `Fetch(engine="scrapling")` |
| Full [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) API | `Fetch(engine="seleniumbase")` |
| Try next engine when blocked | `Fetch(fallback=True)` |
| Shortcuts | `curl_fetch()`, `wreq_fetch()`, `cloudscraper_fetch()`, `seleniumbase_fetch()`, `scrapling_fetch()` |
