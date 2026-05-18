"""Run: uv sync --extra cloudscraper && uv run test_cloudscraper.py"""

from Scraplex import Fetch


def main() -> None:
    fetch = Fetch(engine="cloudscraper")

    scraper = fetch.create_scraper(browser="chrome")
    r = scraper.get("https://httpbin.org/get")
    print("create_scraper.get:", r.status_code, r.json()["url"][:30])

    direct = fetch.CloudScraper()
    r2 = direct.get("https://httpbin.org/headers")
    print("CloudScraper.get:", r2.status_code)



if __name__ == "__main__":
    main()
