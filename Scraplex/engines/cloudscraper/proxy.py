from __future__ import annotations

from types import ModuleType
from typing import Any

from Scraplex.engines.cloudscraper._docs import PROXY_CLASS
from Scraplex.types import EngineId

# Public cloudscraper module surface (no __all__ upstream).
_PUBLIC = (
    "create_scraper",
    "session",
    "get_tokens",
    "get_cookie_string",
    "CloudScraper",
    "CipherSuiteAdapter",
    "Cloudflare",
    "CloudflareIUAMError",
    "CloudflareLoopProtection",
    "User_Agent",
    "captcha",
    "cloudflare",
    "exceptions",
    "interpreters",
    "user_agent",
    "requests",
    "dump",
    "HTTPAdapter",
    "Session",
)


def _pkg() -> ModuleType:
    import cloudscraper

    return cloudscraper


class CloudscraperProxy:
    """cloudscraper module proxy; hover ``fetch`` after ``Fetch(engine=\"cloudscraper\")``."""

    __doc__ = PROXY_CLASS

    def __init__(self) -> None:
        """Bind cloudscraper API; requires Scraplex[cloudscraper]."""
        mod = _pkg()
        object.__setattr__(self, "_module", mod)
        for name in _PUBLIC:
            if hasattr(mod, name):
                object.__setattr__(self, name, getattr(mod, name))
        version = getattr(mod, "__version__", None)
        if version is not None:
            object.__setattr__(self, "__version__", version)

    def __getattr__(self, name: str) -> Any:
        return getattr(object.__getattribute__(self, "_module"), name)

    @property
    def id(self) -> EngineId:
        return "cloudscraper"

    def installed(self) -> bool:
        try:
            _pkg()
            return True
        except ImportError:
            return False
