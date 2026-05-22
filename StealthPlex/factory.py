from __future__ import annotations

from typing import Any, Literal, overload

from StealthPlex.engines.cloudscraper import CloudscraperProxy
from StealthPlex.engines.curl_cffi import CurlCffiProxy
from StealthPlex.engines.docs import apply_fetch_doc
from StealthPlex.engines.seleniumbase import SeleniumBaseProxy
from StealthPlex.engines.scrapling import ScraplingProxy
from StealthPlex.engines.wreq import WreqProxy
from StealthPlex.exceptions import EngineNotImplemented, EngineUnavailable, FetchConfigError
from StealthPlex.fallback_client import FallbackClient
from StealthPlex.types import EngineId


@overload
def Fetch(*, engine: Literal["curl_cffi"]) -> CurlCffiProxy: ...


@overload
def Fetch(*, engine: Literal["wreq"]) -> WreqProxy: ...


@overload
def Fetch(*, engine: Literal["cloudscraper"]) -> CloudscraperProxy: ...


@overload
def Fetch(*, engine: Literal["seleniumbase"]) -> SeleniumBaseProxy: ...


@overload
def Fetch(*, engine: Literal["scrapling"]) -> ScraplingProxy: ...


@overload
def Fetch(
    *,
    engine: None = None,
    fallback: list[EngineId] | None = None,
) -> FallbackClient: ...


def Fetch(
    *,
    engine: EngineId | None = None,
    fallback: list[EngineId] | None = None,
) -> CurlCffiProxy | WreqProxy | CloudscraperProxy | SeleniumBaseProxy | ScraplingProxy | FallbackClient | Any:
    """Create a stealth fetch handle.

    - ``Fetch()`` — auto-stealth fallback chain (curl_cffi → wreq →
      cloudscraper → scrapling → seleniumbase). Tries each engine
      serially until one bypasses. Returns StealthPlex ``Response``.
    - ``Fetch(engine="curl_cffi")`` — bind one upstream library's full API.
    - ``Fetch(fallback=["wreq", "curl_cffi"])`` — custom engine order.

    ``engine=`` and ``fallback=`` are mutually exclusive.
    """
    if engine is not None and fallback is not None:
        raise FetchConfigError("pass engine= or fallback=, not both")

    # --- Bound engine mode ---
    if engine == "curl_cffi":
        proxy = CurlCffiProxy()
        apply_fetch_doc(proxy, engine)
        if not proxy.installed():
            raise EngineUnavailable("curl_cffi", "see README.md for install")
        return proxy

    if engine == "wreq":
        proxy = WreqProxy()
        apply_fetch_doc(proxy, engine)
        if not proxy.installed():
            raise EngineUnavailable("wreq", "see README.md for install")
        return proxy

    if engine == "cloudscraper":
        proxy = CloudscraperProxy()
        apply_fetch_doc(proxy, engine)
        if not proxy.installed():
            raise EngineUnavailable("cloudscraper", "see README.md for install")
        return proxy

    if engine == "seleniumbase":
        proxy = SeleniumBaseProxy()
        apply_fetch_doc(proxy, engine)
        if not proxy.installed():
            raise EngineUnavailable("seleniumbase", "see README.md for install")
        return proxy

    if engine == "scrapling":
        proxy = ScraplingProxy()
        apply_fetch_doc(proxy, engine)
        if not proxy.installed():
            raise EngineUnavailable("scrapling", "see README.md for install")
        return proxy

    if engine is not None:
        raise EngineNotImplemented(engine)

    # --- Stealth fallback mode (default when no engine given) ---
    return FallbackClient(fallback=fallback)
