from __future__ import annotations

from typing import Any, Type

import scrapling.fetchers
import scrapling.parser
import scrapling.spiders
from scrapling.fetchers import (
    AsyncDynamicSession,
    AsyncFetcher,
    AsyncStealthySession,
    DynamicFetcher,
    DynamicSession,
    Fetcher,
    FetcherSession,
    StealthyFetcher,
    StealthySession,
)
from scrapling.parser import Selector, Selectors
from scrapling.spiders import (
    CrawlerEngine,
    CrawlResult,
    CrawlRule,
    CrawlSpider,
    LinkExtractor,
    Request,
    Response,
    Scheduler,
    SessionConfigurationError,
    SessionManager,
    SitemapSpider,
    Spider,
)


class SpidersModule:
    """Type representation of the scrapling.spiders submodule."""

    Spider: Type[Spider]
    CrawlSpider: Type[CrawlSpider]
    SitemapSpider: Type[SitemapSpider]
    Request: Type[Request]
    Response: Type[Response]
    CrawlRule: Type[CrawlRule]
    LinkExtractor: Type[LinkExtractor]
    CrawlResult: Type[CrawlResult]
    Scheduler: Type[Scheduler]
    SessionManager: Type[SessionManager]
    CrawlerEngine: Type[CrawlerEngine]
    SessionConfigurationError: Type[SessionConfigurationError]


class FetchersModule:
    """Type representation of the scrapling.fetchers submodule."""

    Fetcher: Type[Fetcher]
    StealthyFetcher: Type[StealthyFetcher]
    DynamicFetcher: Type[DynamicFetcher]
    AsyncFetcher: Type[AsyncFetcher]
    FetcherSession: Type[FetcherSession]
    StealthySession: Type[StealthySession]
    DynamicSession: Type[DynamicSession]
    AsyncStealthySession: Type[AsyncStealthySession]
    AsyncDynamicSession: Type[AsyncDynamicSession]


class ParserModule:
    """Type representation of the scrapling.parser submodule."""

    Selector: Type[Selector]
    Selectors: Type[Selectors]


class ScraplingProxy:
    """Proxy for scrapling API; exposes fetchers, sessions, spiders, and selectors."""

    Fetcher: Type[Fetcher]
    StealthyFetcher: Type[StealthyFetcher]
    DynamicFetcher: Type[DynamicFetcher]
    AsyncFetcher: Type[AsyncFetcher]
    Selector: Type[Selector]
    spiders: SpidersModule
    fetchers: FetchersModule
    parser: ParserModule

    # Session Classes
    FetcherSession: Type[FetcherSession]
    StealthySession: Type[StealthySession]
    DynamicSession: Type[DynamicSession]
    AsyncStealthySession: Type[AsyncStealthySession]
    AsyncDynamicSession: Type[AsyncDynamicSession]

    @property
    def id(self) -> str:
        """Return engine identifier string."""
        ...

    def installed(self) -> bool:
        """True when dependency is importable."""
        ...

    def __getattr__(self, name: str) -> Any:
        """Retrieve attributes from underlying module."""
        ...
