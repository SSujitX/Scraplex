from typing import Literal, overload

from StealthPlex.engines.cloudscraper.proxy import CloudscraperProxy
from StealthPlex.engines.curl_cffi.proxy import CurlCffiProxy
from StealthPlex.engines.seleniumbase.proxy import SeleniumBaseProxy
from StealthPlex.engines.scrapling.proxy import ScraplingProxy
from StealthPlex.engines.wreq.proxy import WreqProxy
from StealthPlex.fallback_client import FallbackClient
from StealthPlex.types import EngineId


@overload
def Fetch(*, engine: Literal["curl_cffi"], fallback: None = None) -> CurlCffiProxy: ...


@overload
def Fetch(*, engine: Literal["wreq"], fallback: None = None) -> WreqProxy: ...


@overload
def Fetch(*, engine: Literal["cloudscraper"], fallback: None = None) -> CloudscraperProxy: ...


@overload
def Fetch(*, engine: Literal["scrapling"], fallback: None = None) -> ScraplingProxy: ...


@overload
def Fetch(*, engine: Literal["seleniumbase"], fallback: None = None) -> SeleniumBaseProxy: ...


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
) -> CurlCffiProxy | WreqProxy | CloudscraperProxy | ScraplingProxy | SeleniumBaseProxy | FallbackClient:
    """Create a fetch handle bound to one engine or a multi-engine fallback chain.

    Pass ``engine=`` **or** ``fallback=``, not both.

    Args:
        engine: Bind one upstream library (``"curl_cffi"``, ``"wreq"``, ...).
            Hover the return value for engine docs and upstream GitHub link.
        fallback: Multi-engine chain. ``True`` = default order; or explicit engine list.
            Returns StealthPlex ``Response`` with ``.attempts``.
    """
    ...
