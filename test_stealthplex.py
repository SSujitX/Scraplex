"""Run: uv sync --extra stealthplex && uv run test_stealthplex.py"""

from __future__ import annotations

import asyncio
from StealthPlex import Fetch
from rich import print


def test_one_off_fetch() -> None:
    """Test one-off fetch with StealthyFetcher."""
    fetch = Fetch(engine="stealthplex")
    resp = fetch.StealthyFetcher.fetch("https://httpbin.org/ip")
    print(f"[StealthyFetcher] OK! Status: {resp.status}")
    assert resp.status == 200


def test_session_sync() -> None:
    """Test session context manager in sync mode."""
    fetch = Fetch(engine="stealthplex")
    with fetch.FetcherSession(impersonate="chrome") as session:
        resp = session.get("https://httpbin.org/cookies/set?foo=bar")
        print(f"[FetcherSession Sync] OK! Status: {resp.status}, cookies: {resp.cookies}")
        assert resp.status == 200


async def test_session_async() -> None:
    """Test session context manager in async mode."""
    fetch = Fetch(engine="stealthplex")
    async with fetch.FetcherSession(impersonate="chrome") as session:
        resp = await session.get("https://httpbin.org/cookies/set?baz=qux")
        print(f"[FetcherSession Async] OK! Status: {resp.status}, cookies: {resp.cookies}")
        assert resp.status == 200


def test_fallback() -> None:
    """Test fallback client using stealthplex engine."""
    fetch = Fetch(fallback=["stealthplex"])
    resp = fetch.get("https://httpbin.org/headers")
    print(f"[Fallback Client] OK! Status: {resp.status_code}, engine: {resp.engine}")
    assert resp.status_code == 200
    assert resp.engine == "stealthplex"


def main() -> None:
    """Run all stealthplex tests."""
    print("Running stealthplex integration tests...")
    test_one_off_fetch()
    test_session_sync()
    asyncio.run(test_session_async())
    test_fallback()
    print("All stealthplex tests passed successfully!")


if __name__ == "__main__":
    main()
