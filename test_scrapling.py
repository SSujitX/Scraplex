"""Run: uv sync --extra scrapling && uv run test_scrapling.py"""

from __future__ import annotations

import asyncio
from StealthPlex import Fetch
from rich import print


def test_one_off_fetch() -> None:
    """Test one-off fetch with StealthyFetcher."""
    fetch = Fetch(engine="scrapling")
    resp = fetch.StealthyFetcher.fetch("https://httpbin.org/ip")
    print(f"[StealthyFetcher] OK! Status: {resp.status}")
    assert resp.status == 200


def test_session_sync() -> None:
    """Test session context manager in sync mode."""
    fetch = Fetch(engine="scrapling")
    with fetch.FetcherSession(impersonate="chrome") as session:
        resp = session.get("https://httpbin.org/cookies/set?foo=bar")
        print(f"[FetcherSession Sync] OK! Status: {resp.status}, cookies: {resp.cookies}")
        assert resp.status == 200


async def test_session_async() -> None:
    """Test session context manager in async mode."""
    fetch = Fetch(engine="scrapling")
    async with fetch.FetcherSession(impersonate="chrome") as session:
        resp = await session.get("https://httpbin.org/cookies/set?baz=qux")
        print(f"[FetcherSession Async] OK! Status: {resp.status}, cookies: {resp.cookies}")
        assert resp.status == 200


def test_fallback() -> None:
    """Test fallback client using scrapling engine."""
    fetch = Fetch(fallback=["scrapling"])
    resp = fetch.get("https://httpbin.org/headers")
    print(f"[Fallback Client] OK! Status: {resp.status_code}, engine: {resp.engine}")
    assert resp.status_code == 200
    assert resp.engine == "scrapling"


def main() -> None:
    """Run all scrapling tests."""
    print("Running scrapling integration tests...")
    test_one_off_fetch()
    test_session_sync()
    asyncio.run(test_session_async())
    test_fallback()
    print("All scrapling tests passed successfully!")


if __name__ == "__main__":
    main()
