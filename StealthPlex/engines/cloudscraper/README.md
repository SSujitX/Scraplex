# cloudscraper Engine Detail

The **cloudscraper** engine is a Python module designed to bypass Cloudflare's anti-bot page (also known as the "JavaScript Challenge" or "I'm Under Attack" mode) by solving the challenges using a JavaScript interpreter.

- **Upstream Project**: [VeNoMouS/cloudscraper](https://github.com/VeNoMouS/cloudscraper)
- **StealthPlex Layer**: Layer 2 (Bypass Client)
- **Extra Dependency**: `cloudscraper`

---

## 1. Setup

Install the optional engine dependency:

```bash
uv sync --extra cloudscraper
```

---

## 2. API Reference & Usage

Use `Fetch(engine="cloudscraper")` to get a bound `cloudscraper` module proxy. 

### Basic Usage

```python
from StealthPlex import Fetch

fetch = Fetch(engine="cloudscraper")

# 1. Create scraper session (Standard requests.Session derivative)
scraper = fetch.create_scraper(browser="chrome")
response = scraper.get("https://example.com")
print(response.status_code, response.text[:200])

# 2. Instantiate the CloudScraper class directly
scraper_obj = fetch.CloudScraper(interpreter="native")
r = scraper_obj.post("https://httpbin.org/post", json={"data": 123})
print(r.status_code)
```

### Cookie and Token Helpers

You can extract bypass cookies and user-agent strings directly to use in third-party clients (like `curl` or `requests`):

```python
from StealthPlex import Fetch

fetch = Fetch(engine="cloudscraper")

# Get Cloudflare bypass tokens
tokens, user_agent = fetch.get_tokens("https://example.com")
print("Tokens:", tokens)
print("UA:", user_agent)

# Get cookie string format
cookie_str, user_agent = fetch.get_cookie_string("https://example.com")
print("Cookies:", cookie_str)
```

---

## 3. Fallback Client Integration

In the fallback chain (`Fetch(fallback=True)`), `cloudscraper` is the third engine tried. Since it relies on Requests, it carries session context and solves basic Cloudflare challenges without spawning full browser instances, offering a faster alternative to headless browsers.
