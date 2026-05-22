from __future__ import annotations

from typing import TYPE_CHECKING, Any

from StealthPlex.response import Response
from StealthPlex.types import EngineId

if TYPE_CHECKING:
    from requests import Response as RequestsResponse

    from cloudscraper import CloudScraper


def _cloudscraper_cls() -> type[CloudScraper]:
    from cloudscraper import CloudScraper

    return CloudScraper


def _normalize_headers(headers: Any) -> dict[str, str]:
    if headers is None:
        return {}
    return {str(k): str(v) for k, v in headers.items()}


def _normalize_cookies(jar: Any) -> dict[str, str]:
    if jar is None:
        return {}
    try:
        return {cookie.name: cookie.value for cookie in jar}
    except (AttributeError, TypeError):
        return {}


def response_from_cloudscraper(
    upstream: RequestsResponse,
    *,
    engine: EngineId = "cloudscraper",
    attempts: tuple[str, ...] = (),
) -> Response:
    """Build StealthPlex Response from requests/cloudscraper Response."""
    content: bytes = upstream.content or b""
    encoding = upstream.encoding or "utf-8"
    return Response(
        status_code=int(upstream.status_code),
        headers=_normalize_headers(upstream.headers),
        content=content,
        text=content.decode(encoding, errors="replace"),
        url=str(upstream.url),
        cookies=_normalize_cookies(upstream.cookies),
        engine=engine,
        handle=upstream,
        attempts=attempts,
    )


class CloudscraperEngine:
    """cloudscraper engine adapter; create_scraper() session for fallback chain."""

    def __init__(self) -> None:
        self._scraper: CloudScraper | None = None

    @property
    def id(self) -> EngineId:
        return "cloudscraper"

    @property
    def scraper(self) -> CloudScraper:
        if self._scraper is None:
            self._scraper = _cloudscraper_cls().create_scraper()
        return self._scraper

    def installed(self) -> bool:
        try:
            _cloudscraper_cls()
        except ImportError:
            return False
        return True

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> Response:
        """Perform HTTP request via cloudscraper CloudScraper session."""
        req_kwargs: dict[str, Any] = dict(kwargs)
        if headers is not None:
            req_kwargs["headers"] = headers
        if cookies is not None:
            req_kwargs["cookies"] = cookies
        if params is not None:
            req_kwargs["params"] = params
        if data is not None:
            req_kwargs["data"] = data
        if json is not None:
            req_kwargs["json"] = json
        if timeout is not None:
            req_kwargs["timeout"] = timeout

        upstream = self.scraper.request(method.upper(), url, **req_kwargs)
        return response_from_cloudscraper(upstream, attempts=(self.id,))
