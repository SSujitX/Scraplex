from typing import Literal, overload

from StealthPlex.engines.cloudscraper.proxy import CloudscraperProxy
from StealthPlex.engines.curl_cffi.proxy import CurlCffiProxy
from StealthPlex.engines.seleniumbase.proxy import SeleniumBaseProxy
from StealthPlex.engines.scrapling.proxy import ScraplingProxy
from StealthPlex.engines.wreq.proxy import WreqProxy
from StealthPlex.fallback_client import FallbackClient
from StealthPlex.types import EngineId


@overload
def Fetch(*, engine: Literal["curl_cffi"]) -> CurlCffiProxy: ...


@overload
def Fetch(*, engine: Literal["wreq"]) -> WreqProxy: ...


@overload
def Fetch(*, engine: Literal["cloudscraper"]) -> CloudscraperProxy: ...


@overload
def Fetch(*, engine: Literal["scrapling"]) -> ScraplingProxy: ...


@overload
def Fetch(*, engine: Literal["seleniumbase"]) -> SeleniumBaseProxy: ...


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
) -> CurlCffiProxy | WreqProxy | CloudscraperProxy | ScraplingProxy | SeleniumBaseProxy | FallbackClient:
    """Create a stealth fetch handle.

    - ``Fetch()`` — auto-stealth fallback chain (wreq → curl_cffi →
      cloudscraper → scrapling → seleniumbase). Returns StealthPlex ``Response``.
    - ``Fetch(engine=...)`` — bind one upstream library's full API.
    - ``Fetch(fallback=[...])`` — custom engine order.
    """
    ...
