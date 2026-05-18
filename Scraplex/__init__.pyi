from Scraplex.engines.cloudscraper.proxy import CloudscraperProxy
from Scraplex.engines.curl_cffi.proxy import CurlCffiProxy
from Scraplex.engines.wreq.proxy import WreqProxy
from Scraplex.exceptions import (
    ClientConfigError,
    EngineNotImplemented,
    EngineUnavailable,
    EscalationExhausted,
    FetchConfigError,
    FetchError,
    ScraplexError,
)
from Scraplex.factory import Fetch
from Scraplex.fallback_client import FallbackClient
from Scraplex.response import Response
from Scraplex.types import DEFAULT_FALLBACK, EngineId

__version__: str

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
    "ScraplexError",
    "WreqProxy",
    "cloudscraper_fetch",
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
