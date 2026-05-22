# curl_cffi Engine Detail

The **curl_cffi** engine is a Python wrapper for `curl-impersonate` via CFFI, allowing you to perform HTTP requests that mimic real browser TLS profiles (JA3/JA4 signatures) and HTTP/2/3 frames.

- **Upstream Project**: [lexiforest/curl_cffi](https://github.com/lexiforest/curl_cffi)
- **StealthPlex Layer**: Layer 1 (Fast TLS Impersonation Client)
- **Extra Dependency**: `curl_cffi`

---

## 1. Setup

Install the optional engine dependency:

```bash
uv sync --extra curl_cffi
```

---

## 2. API Reference & Usage

Use `Fetch(engine="curl_cffi")` to bind to this engine. It provides a module-level proxy mapping the full `curl_cffi` requests interface.

### Impersonate Signatures

Pass the `impersonate` keyword argument to any request method to select a browser profile:
- `"chrome"` (default Chrome signature)
- `"chrome124"`, `"chrome110"`, `"safari17"`, `"firefox120"`, etc.

### Sync Usage

```python
from StealthPlex import Fetch

fetch = Fetch(engine="curl_cffi")

# Module level one-shot request
resp = fetch.get("https://tls.browserleaks.com/json", impersonate="chrome124")
print(resp.status_code)
print(resp.json())

# Persistent cookies/headers Session
session = fetch.Session(impersonate="chrome124")
try:
    session.get("https://httpbin.org/cookies/set/foo/bar")
    r = session.get("https://httpbin.org/cookies")
    print(r.json())
finally:
    session.close()
```

### Async Usage

All async requests are located under the `.aio` namespace (or inside `AsyncSession`):

```python
import asyncio
from StealthPlex import Fetch

async def main():
    fetch = Fetch(engine="curl_cffi")

    # Async one-shot request
    r = await fetch.aio.get("https://httpbin.org/get", impersonate="chrome124")
    print("One-shot status:", r.status_code)

    # Async Session
    async with fetch.AsyncSession(impersonate="chrome124") as session:
        r = await session.get("https://httpbin.org/get")
        print("Session status:", r.status_code)

asyncio.run(main())
```

### WebSockets

Access standard or async WebSockets:
```python
ws = fetch.WebSocket("wss://example.com/socket")
# Or async version: fetch.AsyncWebSocket
```

---

## 3. Fallback Client Integration

In the fallback escalation chain (`Fetch(fallback=True)`), `curl_cffi` is the second engine tried if `wreq` fails. It maintains cookie consistency across transitions and impersonates a Chrome browser.
