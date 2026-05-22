# wreq Engine Detail

The **wreq** engine is a high-performance, Rust-backed HTTP client optimized for async browser impersonation and TLS/JA3 fingerprint evasion.

- **Upstream Project**: [0x676e67/wreq-python](https://github.com/0x676e67/wreq-python)
- **StealthPlex Layer**: Layer 1 (Fast HTTP/2 Impersonation Client)
- **Extra Dependency**: `wreq`

---

## 1. Setup

Install the optional engine dependency:

```bash
uv sync --extra wreq
```

---

## 2. API Reference & Usage

Use `Fetch(engine="wreq")` to get a bound `wreq` module proxy. It exposes the raw package API and types.

### Emulation Modes

You can specify a targeted browser signature to spoof via `fetch.Emulation`:
- `fetch.Emulation.Firefox149`
- `fetch.Emulation.Chrome131`
- And all other signatures supported upstream.

### Async Example (Default)

```python
import asyncio
from StealthPlex import Fetch

async def main():
    fetch = Fetch(engine="wreq")
    
    # 1. Module-level async request
    response = await fetch.get(
        "https://httpbin.org/get", 
        emulation=fetch.Emulation.Firefox149
    )
    print("Status:", response.status)
    print("Content:", await response.text())

    # 2. Async persistent client
    client = fetch.Client(emulation=fetch.Emulation.Chrome131)
    try:
        r = await client.get("https://httpbin.org/get")
        print("Body:", await r.text())
    finally:
        client.close()

asyncio.run(main())
```

### Sync Example (Blocking)

```python
from StealthPlex import Fetch

fetch = Fetch(engine="wreq")

# Blocking client for synchronous scripts
client = fetch.blocking.Client(emulation=fetch.Emulation.Firefox149)
try:
    response = client.get("https://httpbin.org/get")
    print("Status:", response.status)
    print("Text:", response.text())
finally:
    client.close()
```

---

## 3. Fallback Client Integration

When using `Fetch(fallback=True)`, StealthPlex uses `wreq` as the very first step in the fallback chain. It performs a fast, lightweight HTTP request using a default browser profile, escaping basic bot/fingerprinting hurdles.
