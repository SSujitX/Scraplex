# Scrapling Engine Detail

The **scrapling** engine is an adaptive web scraping and stealth crawling framework built for sites with advanced anti-bot protections and dynamic layouts. It manages chromium-based browser instances under the hood, solving Turnstile challenges and spoofing advanced browser fingerprints.

- **Upstream Project**: [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling)
- **StealthPlex Layer**: Layer 3 (Stealth / Crawl Browser Tier)
- **Extra Dependency**: `scrapling`

---

## 1. Setup

Install the optional engine dependency:

```bash
uv sync --extra scrapling
```

> [!NOTE]
> On first run, Scrapling will automatically download and install its browser binaries if they are missing on your system.

---

## 2. API Reference & Usage

Use `Fetch(engine="scrapling")` to get a bound `scrapling` proxy handle. It exposes the full Scrapling class suite including Fetchers, Sessions, and Spiders.

### Exposing `.fetcher` shortcut
Per the StealthPlex API rules, the `.fetcher` attribute on the `fetch` variable is mapped directly to `StealthyFetcher`, allowing:
`fetch.fetcher.fetch("https://example.com", headless=False)`

### 1. Stealth One-Off Fetch (Sync & Async)

```python
import asyncio
from StealthPlex import Fetch

fetch = Fetch(engine="scrapling")

# Sync one-off stealth fetch
resp = fetch.StealthyFetcher.fetch(
    "https://nowsecure.nl",
    solve_cloudflare=True,   # Solve Turnstile/Interstitial challenge
    block_webrtc=True,       # Prevent IP/DNS leaks via WebRTC
    hide_canvas=True,        # Avoid canvas fingerprinting
    dns_over_https=True,     # Route DNS queries via DoH
    block_ads=True,          # Block tracking/ad scripts to load faster
    headless=False           # Runs in headed mode for maximum stealth
)
print("Status:", resp.status)
# Scrapling response allows BeautifulSoup-like Selector/XPath calls automatically:
print(resp.xpath('//h1/text()').get())

# Async one-shot stealth fetch
async def run_async():
    r = await fetch.StealthyFetcher.async_fetch(
        "https://nowsecure.nl",
        solve_cloudflare=True,
        headless=False
    )
    print("Async Status:", r.status)

asyncio.run(run_async())
```

### 2. Persistent Sessions (Sync & Async)

Reuse the browser context, cookies, and fingerprint headers across multiple requests:

```python
from StealthPlex import Fetch

fetch = Fetch(engine="scrapling")

with fetch.StealthySession(solve_cloudflare=True, headless=False) as session:
    # Solves CF Turnstile and sets authenticated cookies
    r1 = session.get("https://nowsecure.nl")
    print("Page 1:", r1.status)
    
    # Reuses browser state for subsequent pages
    r2 = session.get("https://nowsecure.nl/another-page")
    print("Page 2:", r2.status)
```

For async sessions, use `AsyncStealthySession`:
```python
async with fetch.AsyncStealthySession(solve_cloudflare=True, headless=False) as session:
    r = await session.get("https://nowsecure.nl")
```

### 3. Spider Crawling Framework

You can define and run large concurrent crawling jobs using Scrapling's built-in Spider architecture:

```python
from StealthPlex import Fetch

fetch = Fetch(engine="scrapling")

class MyStealthSpider(fetch.spiders.Spider):
    name = "my_spider"
    start_urls = ["https://httpbin.org/html"]

    def parse(self, response):
        # response has full parsing capability
        title = response.xpath("//h1/text()").get()
        print("Scraped title:", title)

spider = MyStealthSpider()
spider.start()
```

---

## 3. Fallback Client Integration

In the fallback chain (`Fetch(fallback=True)`), `scrapling` is the fourth engine tried. If simple requests, TLS impersonation, and script-based bypasses fail, StealthPlex escalates to `scrapling` to spin up a stealthy headed browser (using xvfb-run or Xvfb on Linux for background execution), execute JavaScript, and bypass Turnstile challenges.
