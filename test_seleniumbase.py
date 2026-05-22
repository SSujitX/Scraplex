"""Run: uv sync --extra seleniumbase && uv run test_seleniumbase.py"""

import asyncio
from Scraplex import Fetch


def test_with_cdp() -> None:
    """Verify using with fetch.SB(...) context manager + activate_cdp_mode()."""
    fetch = Fetch(engine="seleniumbase")

    with fetch.SB(uc=True, test=True) as sb:
        url = "https://seleniumbase.io/demo_page"
        sb.activate_cdp_mode(url)
        sb.sleep(1.0)

        # Interact using stealthy CDP methods on sb.cdp
        sb.cdp.type("input#myTextInput", "Stealthy context manager")
        sb.cdp.click("input#checkBox1")

        header_text = sb.cdp.get_text("h1")
        print(f"[With CDP] OK! Header: {header_text}")


def test_raw_cdp() -> None:
    """Verify using raw CDP (Pure CDP Mode) via fetch.sb_cdp."""
    fetch = Fetch(engine="seleniumbase")

    # Initialize raw browser using pure CDP mode (no WebDriver)
    url = "https://seleniumbase.io/demo_page"
    sb = fetch.sb_cdp.Chrome(url)
    try:
        sb.sleep(1.0)

        # Interact using CDP methods directly on the browser object
        sb.type("input#myTextInput", "Pure Raw CDP Mode")
        sb.click("input#checkBox1")

        header_text = sb.get_text("h1")
        print(f"[Raw CDP] OK! Header: {header_text}")
    finally:
        # Always stop the driver to clean up the browser process
        sb.driver.stop()


def test_cloudflare_bypass_with_cdp() -> None:
    """Verify bypassing Cloudflare Turnstile using With CDP mode."""
    fetch = Fetch(engine="seleniumbase")

    with fetch.SB(uc=True, test=True) as sb:
        url = "https://seleniumbase.io/apps/turnstile"
        sb.activate_cdp_mode(url)
        sb.sleep(2.0)

        # Solve Turnstile challenge via CDP
        sb.solve_captcha()
        sb.sleep(2.0)

        # Verify success
        if sb.cdp.is_element_visible("img#captcha-success"):
            print("[CF Bypass With CDP] Success!")
        else:
            raise RuntimeError("Failed to bypass Turnstile in With CDP mode")


def test_cloudflare_bypass_raw_cdp() -> None:
    """Verify bypassing Cloudflare Turnstile using Raw CDP sync mode."""
    fetch = Fetch(engine="seleniumbase")

    url = "https://seleniumbase.io/apps/turnstile"
    sb = fetch.sb_cdp.Chrome(url)
    try:
        sb.sleep(2.0)

        # Solve Turnstile challenge
        sb.solve_captcha()
        sb.sleep(2.0)

        # Verify success
        if sb.is_element_visible("img#captcha-success"):
            print("[CF Bypass Raw CDP Sync] Success!")
        else:
            raise RuntimeError("Failed to bypass Turnstile in Raw CDP sync mode")
    finally:
        sb.driver.stop()


async def test_cloudflare_bypass_async_cdp() -> None:
    """Verify bypassing Cloudflare Turnstile using Raw CDP async mode."""
    fetch = Fetch(engine="seleniumbase")

    url = "https://seleniumbase.io/apps/turnstile"
    driver = await fetch.cdp_driver.start_async(headless=False)
    try:
        tab = driver.page
        await tab.get(url)
        await tab.sleep(2.0)

        # Solve Turnstile challenge asynchronously
        await tab.solve_captcha()
        await tab.sleep(2.0)

        # Verify success
        if await tab.is_element_visible("img#captcha-success"):
            print("[CF Bypass Raw CDP Async] Success!")
        else:
            raise RuntimeError("Failed to bypass Turnstile in Raw CDP async mode")
    finally:
        driver.stop()


def main() -> None:
    try:
        test_with_cdp()
    except Exception as exc:
        print("[With CDP] failed:", exc)

    try:
        test_raw_cdp()
    except Exception as exc:
        print("[Raw CDP] failed:", exc)

    try:
        test_cloudflare_bypass_with_cdp()
    except Exception as exc:
        print("[CF Bypass With CDP] failed:", exc)

    try:
        test_cloudflare_bypass_raw_cdp()
    except Exception as exc:
        print("[CF Bypass Raw CDP] failed:", exc)

    try:
        asyncio.run(test_cloudflare_bypass_async_cdp())
    except Exception as exc:
        print("[CF Bypass Async CDP] failed:", exc)


if __name__ == "__main__":
    main()

