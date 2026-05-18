from Scraplex.engines.cloudscraper import CloudscraperProxy
from Scraplex.engines.curl_cffi import CurlCffiProxy
from Scraplex.engines.wreq import WreqProxy
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


def curl_fetch() -> CurlCffiProxy:
    """Return curl_cffi proxy; same as ``Fetch(engine=\"curl_cffi\")``."""
    return Fetch(engine="curl_cffi")


def wreq_fetch() -> WreqProxy:
    """Return wreq proxy; same as ``Fetch(engine=\"wreq\")``."""
    return Fetch(engine="wreq")


def cloudscraper_fetch() -> CloudscraperProxy:
    """Return cloudscraper proxy; same as ``Fetch(engine=\"cloudscraper\")``."""
    return Fetch(engine="cloudscraper")


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

__version__ = "0.1.0"
