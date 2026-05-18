from __future__ import annotations

from dataclasses import dataclass

from Scraplex.types import EngineId


@dataclass(frozen=True, slots=True)
class EngineInfo:
    """Per-engine metadata for proxy hover docs (install steps live in README.md)."""

    title: str
    github: str
    extra: str
    summary: str
    handle: str
    examples: str


ENGINE_INFO: dict[EngineId, EngineInfo] = {
    "wreq": EngineInfo(
        title="wreq",
        github="https://github.com/0x676e67/wreq-python",
        extra="wreq",
        summary="Rust-backed HTTP client with browser impersonation (Layer 1).",
        handle="``await fetch.get(...)``, ``fetch.Client(...)``, ``fetch.blocking.Client`` for sync.",
        examples="""    import asyncio
    async def main():
        fetch = Fetch(engine="wreq")
        r = await fetch.get("https://example.com", emulation=fetch.Emulation.Firefox149)
        print(await r.text())
    asyncio.run(main())""",
    ),
    "curl_cffi": EngineInfo(
        title="curl_cffi",
        github="https://github.com/lexiforest/curl_cffi",
        extra="curl_cffi",
        summary="Same API as ``import curl_cffi`` (TLS/JA3 impersonation, HTTP/2/3).",
        handle="``fetch.get`` (sync), ``await fetch.aio.get`` (async), ``fetch.Session``, ``fetch.AsyncSession``.",
        examples="""    fetch = Fetch(engine="curl_cffi")
    r = fetch.get("https://example.com", impersonate="chrome")
    r = await fetch.aio.get("https://example.com", impersonate="chrome")
    async with fetch.AsyncSession(impersonate="chrome124") as s:
        r = await s.get("https://example.com")""",
    ),
    "cloudscraper": EngineInfo(
        title="cloudscraper",
        github="https://github.com/VeNoMouS/cloudscraper",
        extra="cloudscraper",
        summary="Cloudflare-aware scraper built on requests (Layer 2).",
        handle="``fetch.create_scraper().get(...)``, ``fetch.CloudScraper()``, ``fetch.get_tokens(url)``.",
        examples="""    fetch = Fetch(engine="cloudscraper")
    scraper = fetch.create_scraper(browser="chrome")
    r = scraper.get("https://example.com")
    tokens, ua = fetch.get_tokens("https://example.com")""",
    ),
    "scrapling": EngineInfo(
        title="scrapling",
        github="https://github.com/D4Vinci/Scrapling",
        extra="scrapling",
        summary="Stealth fetcher with headless browser support (Layer 3).",
        handle="``fetch.fetcher.fetch(...)`` for stealth / dynamic pages.",
        examples="""    fetch = Fetch(engine="scrapling")
    r = fetch.fetcher.fetch("https://example.com", headless=True)""",
    ),
    "seleniumbase": EngineInfo(
        title="seleniumbase",
        github="https://github.com/seleniumbase/SeleniumBase",
        extra="seleniumbase",
        summary="Browser automation for hard targets (Layer 4).",
        handle="``with fetch.sb as sb: sb.open(url)`` context manager.",
        examples="""    fetch = Fetch(engine="seleniumbase")
    with fetch.sb as sb:
        sb.open("https://example.com")""",
    ),
}

def proxy_doc(engine_id: EngineId) -> str:
    """Docstring for bound engine handle — shown when hovering the ``fetch`` variable."""
    info = ENGINE_INFO[engine_id]
    return f"""{info.title} — {info.summary}

Use {info.handle}
Returns upstream library types (not Scraplex ``Response``).

Docs & use cases: {info.github}

Examples:
{info.examples}
"""


def apply_fetch_doc(obj: object, engine_id: EngineId) -> None:
    """Set runtime __doc__ on engine-bound fetch handle for hover after assignment."""
    obj.__doc__ = proxy_doc(engine_id)
