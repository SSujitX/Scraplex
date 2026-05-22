from __future__ import annotations

from typing import TYPE_CHECKING, Any

from StealthPlex.response import Response
from StealthPlex.types import EngineId

if TYPE_CHECKING:
    from curl_cffi.requests import Response as CurlResponse
    from curl_cffi.requests import Session


def _import_curl_cffi_session() -> type[Session]:
    """Import curl_cffi Session; raises ImportError when extra is missing."""
    from curl_cffi.requests import Session

    return Session


def _normalize_headers(headers: Any) -> dict[str, str]:
    """Convert curl_cffi headers mapping to plain str dict."""
    if headers is None:
        return {}
    return {str(key): str(value) for key, value in headers.items()}


def _normalize_cookies(jar: Any) -> dict[str, str]:
    """Extract cookie name/value pairs from curl_cffi cookie jar."""
    if jar is None:
        return {}
    try:
        return {cookie.name: cookie.value for cookie in jar}
    except (AttributeError, TypeError):
        return {}


def response_from_curl(
    upstream: CurlResponse,
    *,
    engine: EngineId = "curl_cffi",
    attempts: tuple[str, ...] = (),
) -> Response:
    """Build StealthPlex Response from curl_cffi Response; upstream raw response object."""
    content: bytes = upstream.content or b""
    return Response(
        status_code=int(upstream.status_code),
        headers=_normalize_headers(upstream.headers),
        content=content,
        text=content.decode(upstream.encoding or "utf-8", errors="replace"),
        url=str(upstream.url),
        cookies=_normalize_cookies(upstream.cookies),
        engine=engine,
        handle=upstream,
        attempts=attempts,
    )


class CurlCffiEngine:
    """curl_cffi engine adapter; session.request for StealthPlex fallback chain."""

    def __init__(self) -> None:
        self._session: Session | None = None

    @property
    def id(self) -> EngineId:
        """Return engine identifier curl_cffi."""
        return "curl_cffi"

    @property
    def session(self) -> Session:
        """Return curl_cffi Session with Chrome impersonation enabled."""
        if self._session is None:
            self._session = _import_curl_cffi_session()(impersonate="chrome")
        return self._session

    def installed(self) -> bool:
        """Return True when curl-cffi package is installed."""
        try:
            _import_curl_cffi_session()
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
        """Perform HTTP request via session.request; kwargs forwarded to curl_cffi."""
        upstream = self.session.request(
            method=method.upper(),
            url=url,
            headers=headers,
            cookies=cookies,
            params=params,
            data=data,
            json=json,
            timeout=timeout,
            **kwargs,
        )
        return response_from_curl(upstream, attempts=(self.id,))
