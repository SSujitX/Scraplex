from StealthPlex.engines.cloudscraper.proxy import CloudscraperProxy
from StealthPlex.engines.curl_cffi.proxy import CurlCffiProxy
from StealthPlex.engines.seleniumbase.proxy import SeleniumBaseProxy
from StealthPlex.engines.scrapling.proxy import ScraplingProxy
from StealthPlex.engines.wreq.proxy import WreqProxy
from StealthPlex.exceptions import (
    ClientConfigError,
    EngineNotImplemented,
    EngineUnavailable,
    EscalationExhausted,
    FetchConfigError,
    FetchError,
    StealthPlexError,
)
from StealthPlex.factory import Fetch
from StealthPlex.fallback_client import FallbackClient
from StealthPlex.response import Response
from StealthPlex.types import DEFAULT_FALLBACK, EngineId

__all__ = [
    "DEFAULT_FALLBACK",
    "CloudscraperProxy",
    "CurlCffiProxy",
    "FallbackClient",
    "Fetch",
    "FetchConfigError",
    "ClientConfigError",
    "EngineId",
    "EngineNotImplemented",
    "EngineUnavailable",
    "EscalationExhausted",
    "FetchError",
    "Response",
    "StealthPlexError",
    "SeleniumBaseProxy",
    "ScraplingProxy",
    "WreqProxy",
    "cloudscraper_fetch",
    "seleniumbase_fetch",
    "scrapling_fetch",
    "curl_fetch",
    "wreq_fetch",
]


def curl_fetch() -> CurlCffiProxy:
    """Shortcut for ``Fetch(engine=\"curl_cffi\")``."""
    ...


def wreq_fetch() -> WreqProxy:
    """Shortcut for ``Fetch(engine=\"wreq\")``."""
    ...


def cloudscraper_fetch() -> CloudscraperProxy:
    """Shortcut for ``Fetch(engine=\"cloudscraper\")``."""
    ...


def seleniumbase_fetch() -> SeleniumBaseProxy:
    """Shortcut for ``Fetch(engine=\"seleniumbase\")``."""
    ...


def scrapling_fetch() -> ScraplingProxy:
    """Shortcut for ``Fetch(engine=\"scrapling\")``."""
    ...
