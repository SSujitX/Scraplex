from __future__ import annotations

from typing import TYPE_CHECKING, Any

from StealthPlex.response import Response
from StealthPlex.types import EngineId

if TYPE_CHECKING:
    from wreq.blocking import Client as BlockingClient
    from wreq.blocking import Response as WreqResponse


def _blocking_client() -> type[BlockingClient]:
    from wreq.blocking import Client

    return Client


def _normalize_headers(headers: Any) -> dict[str, str]:
    if headers is None:
        return {}
    if hasattr(headers, "items"):
        return {str(k): str(v) for k, v in headers.items()}
    return {}


def _normalize_cookies(cookies: Any) -> dict[str, str]:
    if cookies is None:
        return {}
    out: dict[str, str] = {}
    try:
        for cookie in cookies:
            out[str(cookie.name)] = str(cookie.value)
    except (AttributeError, TypeError):
        return {}
    return out


def response_from_wreq(
    upstream: WreqResponse,
    *,
    engine: EngineId = "wreq",
    attempts: tuple[str, ...] = (),
) -> Response:
    """Build StealthPlex Response from wreq blocking Response."""
    content = upstream.bytes()
    status = upstream.status.as_int() if hasattr(upstream.status, "as_int") else int(upstream.status)
    return Response(
        status_code=status,
        headers=_normalize_headers(upstream.headers),
        content=content,
        text=upstream.text(),
        url=str(upstream.url),
        cookies=_normalize_cookies(upstream.cookies),
        engine=engine,
        handle=upstream,
        attempts=attempts,
    )


class WreqEngine:
    """wreq engine adapter; blocking.Client for StealthPlex fallback chain."""

    def __init__(self) -> None:
        self._client: BlockingClient | None = None

    @property
    def id(self) -> EngineId:
        return "wreq"

    @property
    def client(self) -> BlockingClient:
        if self._client is None:
            self._client = _blocking_client()()
        return self._client

    def installed(self) -> bool:
        try:
            _blocking_client()
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
        """Perform HTTP request via wreq.blocking.Client."""
        from wreq import Method

        method_map = {
            "GET": Method.GET,
            "POST": Method.POST,
            "PUT": Method.PUT,
            "PATCH": Method.PATCH,
            "DELETE": Method.DELETE,
            "HEAD": Method.HEAD,
            "OPTIONS": Method.OPTIONS,
            "TRACE": Method.TRACE,
        }
        wreq_method = method_map.get(method.upper(), Method.GET)
        req_kwargs: dict[str, Any] = dict(kwargs)
        if headers is not None:
            req_kwargs["headers"] = headers
        if json is not None:
            req_kwargs["json"] = json
        if data is not None:
            req_kwargs["body"] = data
        if params is not None:
            req_kwargs["query"] = params
        if timeout is not None:
            import datetime

            req_kwargs["timeout"] = datetime.timedelta(seconds=timeout)
        if cookies:
            req_kwargs["cookies"] = cookies

        upstream = self.client.request(wreq_method, url, **req_kwargs)
        return response_from_wreq(upstream, attempts=(self.id,))
