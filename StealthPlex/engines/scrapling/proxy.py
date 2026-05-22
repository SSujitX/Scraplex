from __future__ import annotations

from types import ModuleType
from typing import Any

from StealthPlex.engines.scrapling._docs import PROXY_CLASS
from StealthPlex.types import EngineId


def _pkg() -> ModuleType:
    import scrapling

    return scrapling


class ScraplingProxy:
    """Proxy for scrapling API; exposes fetchers, sessions, spiders, and selectors."""

    __doc__ = PROXY_CLASS

    def __init__(self) -> None:
        """Bind scrapling API; requires StealthPlex[scrapling]."""
        from StealthPlex.engines.scrapling.engine import _ensure_dependencies

        _ensure_dependencies()
        mod = _pkg()
        import scrapling.fetchers
        import scrapling.spiders
        import scrapling.parser

        object.__setattr__(self, "_module", mod)
        object.__setattr__(self, "Fetcher", mod.Fetcher)
        object.__setattr__(self, "StealthyFetcher", mod.StealthyFetcher)
        object.__setattr__(self, "fetcher", mod.StealthyFetcher)
        object.__setattr__(self, "DynamicFetcher", mod.DynamicFetcher)
        object.__setattr__(self, "AsyncFetcher", mod.AsyncFetcher)
        object.__setattr__(self, "Selector", mod.Selector)
        object.__setattr__(self, "spiders", mod.spiders)
        object.__setattr__(self, "fetchers", scrapling.fetchers)
        object.__setattr__(self, "parser", scrapling.parser)

        # Bind all session classes
        for name in (
            "FetcherSession",
            "StealthySession",
            "DynamicSession",
            "AsyncStealthySession",
            "AsyncDynamicSession",
        ):
            if hasattr(scrapling.fetchers, name):
                object.__setattr__(self, name, getattr(scrapling.fetchers, name))

    def __getattr__(self, name: str) -> Any:
        return getattr(object.__getattribute__(self, "_module"), name)

    @property
    def id(self) -> EngineId:
        return "scrapling"

    def installed(self) -> bool:
        try:
            _pkg()
            return True
        except ImportError:
            return False
