from __future__ import annotations

from typing import Any, Literal, overload

from Scraplex.engines.cloudscraper import CloudscraperProxy
from Scraplex.engines.curl_cffi import CurlCffiProxy
from Scraplex.engines.docs import apply_fetch_doc
from Scraplex.engines.wreq import WreqProxy
from Scraplex.exceptions import EngineNotImplemented, EngineUnavailable, FetchConfigError
from Scraplex.fallback_client import FallbackClient
from Scraplex.types import EngineId


@overload
def Fetch(*, engine: Literal["curl_cffi"], fallback: None = None) -> CurlCffiProxy: ...


@overload
def Fetch(*, engine: Literal["wreq"], fallback: None = None) -> WreqProxy: ...


@overload
def Fetch(*, engine: Literal["cloudscraper"], fallback: None = None) -> CloudscraperProxy: ...


@overload
def Fetch(
    *,
    engine: Literal["scrapling", "seleniumbase"],
    fallback: None = None,
) -> Any: ...


@overload
def Fetch(
    *,
    engine: None = None,
    fallback: bool | list[EngineId],
) -> FallbackClient: ...


def Fetch(
    *,
    engine: EngineId | None = None,
    fallback: bool | list[EngineId] | None = None,
) -> CurlCffiProxy | WreqProxy | CloudscraperProxy | FallbackClient | Any:
    """Create a fetch handle bound to one engine or a multi-engine fallback chain.

    Pass ``engine=`` **or** ``fallback=``, not both.

    Args:
        engine: Bind one upstream library (``"curl_cffi"``, ``"wreq"``, ...).
            Returns that library's API — hover the return value for engine docs.
        fallback: Multi-engine chain. ``True`` = default order; or a list of engine ids.
            Returns Scraplex ``Response`` with ``.attempts``.
    """
    if engine is not None and fallback is not None:
        raise FetchConfigError("pass engine= or fallback=, not both")
    if engine is None and fallback is None:
        raise FetchConfigError("pass engine= or fallback=")

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

    if engine is not None:
        raise EngineNotImplemented(engine)

    return FallbackClient(fallback=fallback)
