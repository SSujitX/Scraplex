"""Run: uv sync --extra wreq && uv run test_wreq.py"""

import asyncio

from StealthPlex import Fetch


async def main() -> None:
    fetch = Fetch(engine="wreq")
    r = await fetch.get("https://httpbin.org/get", emulation=fetch.Emulation.Firefox149)
    print("status:", r.status)
    print("body:", (await r.text())[:80])


if __name__ == "__main__":
    asyncio.run(main())
