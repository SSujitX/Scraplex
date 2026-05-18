"""Run: uv sync --extra curl_cffi && uv run test_curl_cffi_async.py"""

import asyncio

from Scraplex import Fetch


async def main() -> None:
    fetch = Fetch(engine="curl_cffi")

    r = await fetch.aio.get("https://httpbin.org/get", impersonate="chrome")
    print("aio.get:", r.status_code)

    async with fetch.AsyncSession(impersonate="chrome124") as session:
        r2 = await session.get("https://httpbin.org/get")
        print("AsyncSession:", r2.status_code, r2.json()["url"][:30])


if __name__ == "__main__":
    asyncio.run(main())
