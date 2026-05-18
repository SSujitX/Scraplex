"""IDE stubs for engines not yet implemented — hover ``fetch`` shows engine-specific docs."""


class ScraplingProxy:
    """scrapling — Stealth fetcher with headless browser support (Layer 3).

    Use ``fetch.fetcher.fetch(...)`` for stealth / dynamic pages.
    Docs & use cases: https://github.com/D4Vinci/Scrapling
    """

    def __getattr__(self, name: str) -> object: ...


class SeleniumBaseProxy:
    """seleniumbase — Browser automation for hard targets (Layer 4).

    Use ``with fetch.sb as sb: sb.open(url)``.
    Docs & use cases: https://github.com/seleniumbase/SeleniumBase
    """

    def __getattr__(self, name: str) -> object: ...
