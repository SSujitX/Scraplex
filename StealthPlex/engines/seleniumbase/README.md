# SeleniumBase Engine Detail

The **seleniumbase** engine is the ultimate, hard-target browser automation layer in StealthPlex. For highly protected pages that block normal scraping tools, SeleniumBase utilizes **UC (Undetected ChromeDriver) Mode** coupled with **CDP (Chrome DevTools Protocol) Mode** to route actions directly through the browser's developer interface.

- **Upstream Project**: [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
- **StealthPlex Layer**: Layer 4 (Hard Target / Full Browser Automation)
- **Extra Dependency**: `seleniumbase`

---

## 1. Setup

Install the optional engine dependency:

```bash
uv sync --extra seleniumbase
```

---

## 2. API Reference & Usage

Use `Fetch(engine="seleniumbase")` to get a bound `seleniumbase` proxy handle.

### Mode A: UC Mode + CDP Mode (With Context Manager)

This is the standard stealth context manager flow. Calling `sb.activate_cdp_mode(url)` disconnects the WebDriver process and executes actions directly through the Chrome DevTools Protocol to evade active detections.

```python
from StealthPlex import Fetch

fetch = Fetch(engine="seleniumbase")

with fetch.SB(uc=True, test=True) as sb:
    # Navigate using UC + CDP Mode
    url = "https://seleniumbase.io/apps/turnstile"
    sb.activate_cdp_mode(url)
    sb.sleep(2.0)

    # Solve the Turnstile/CAPTCHA challenge
    sb.solve_captcha()
    sb.sleep(2.0)

    # Perform CDP-based interaction
    if sb.cdp.is_element_visible("img#captcha-success"):
         print("Bypassed Cloudflare successfully!")
```

Common CDP method calls on `sb.cdp`:
* `sb.cdp.click(selector)`
* `sb.cdp.type(selector, text)`
* `sb.cdp.gui_click_element(selector)` (Emulates physical user clicking via PyAutoGUI)
* `sb.cdp.solve_captcha()`

### Mode B: Pure CDP Mode (Raw CDP Sync)

Uses a pure Chrome DevTools Protocol session directly without any WebDriver process initialization overhead.

```python
from StealthPlex import Fetch

fetch = Fetch(engine="seleniumbase")

# Start pure CDP browser session
sb = fetch.sb_cdp.Chrome("https://seleniumbase.io/apps/turnstile")
try:
    sb.sleep(2.0)
    sb.solve_captcha()
    sb.sleep(2.0)
    if sb.is_element_visible("img#captcha-success"):
        print("Success! Bypassed Turnstile via Raw CDP Sync mode.")
finally:
    sb.driver.stop()  # Clean up process
```

### Mode C: Async Pure CDP Mode (Raw CDP Async)

You can run Raw CDP mode asynchronously by using the `cdp_driver` module:

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

        # Solve Turnstile challenge asynchronously
        await tab.solve_captcha()
        await tab.sleep(2.0)

        if await tab.is_element_visible("img#captcha-success"):
            print("Success! Bypassed Turnstile via Raw CDP Async mode.")
    finally:
        driver.stop()  # Synchronous clean up call

asyncio.run(main())
```

---

## 3. Fallback Client Integration

In the fallback chain (`Fetch(fallback=True)`), `seleniumbase` is the final engine (Layer 4). Because browser automation is heavy and resource-intensive, StealthPlex only falls back to `seleniumbase` when all other engines fail. During fallback requests it uses the same UC/CDP flow as above: `activate_cdp_mode(url)`, wait, `solve_captcha()` (default on; pass `solve_captcha=False` to skip), wait again, then return page HTML. On Linux, Xvfb is enabled automatically when headed display is unavailable.

