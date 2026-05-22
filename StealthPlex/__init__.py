from StealthPlex.engines.cloudscraper import CloudscraperProxy
from StealthPlex.engines.curl_cffi import CurlCffiProxy
from StealthPlex.engines.seleniumbase import SeleniumBaseProxy
from StealthPlex.engines.scrapling import ScraplingProxy
from StealthPlex.engines.wreq import WreqProxy
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


def curl_fetch() -> CurlCffiProxy:
    """Return curl_cffi proxy; same as ``Fetch(engine=\"curl_cffi\")``."""
    return Fetch(engine="curl_cffi")


def wreq_fetch() -> WreqProxy:
    """Return wreq proxy; same as ``Fetch(engine=\"wreq\")``."""
    return Fetch(engine="wreq")


def cloudscraper_fetch() -> CloudscraperProxy:
    """Return cloudscraper proxy; same as ``Fetch(engine=\"cloudscraper\")``."""
    return Fetch(engine="cloudscraper")


def seleniumbase_fetch() -> SeleniumBaseProxy:
    """Return seleniumbase proxy; same as ``Fetch(engine=\"seleniumbase\")``."""
    return Fetch(engine="seleniumbase")


def scrapling_fetch() -> ScraplingProxy:
    """Return scrapling proxy; same as ``Fetch(engine=\"scrapling\")``."""
    return Fetch(engine="scrapling")


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

__version__ = "0.1.0"
