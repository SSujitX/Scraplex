from __future__ import annotations

from typing import Any

from Scraplex.engines.registry import create_engine, installed_engine_ids
from Scraplex.exceptions import EscalationExhausted, EngineUnavailable
from Scraplex.fallback import resolve_fallback_chain, should_escalate
from Scraplex.response import Response
from Scraplex.session import Session
from Scraplex.types import EngineId

FALLBACK_DOC = """Multi-engine fallback — returns Scraplex ``Response``.

Tries engines in order (``fallback=True`` uses DEFAULT_FALLBACK: wreq → curl_cffi →
cloudscraper → scrapling → seleniumbase).

Returns Scraplex ``Response`` with ``.engine``, ``.attempts``, ``.handle``.

Example:
    fetch = Fetch(fallback=True)
    r = fetch.get("https://example.com")
"""


class FallbackClient:
    """Multi-engine fallback; get/post/request return Scraplex Response."""

    __doc__ = FALLBACK_DOC

    def __init__(
        self,
        *,
        fallback: bool | list[EngineId],
    ) -> None:
        """Init fallback client; fallback True uses DEFAULT_FALLBACK order."""
        self._state = Session()
        self._fallback_use_default = fallback is True
        self._fallback_explicit = fallback if isinstance(fallback, list) else None

    def get(self, url: str, **kwargs: Any) -> Response:
        """HTTP GET with fallback chain; url target, kwargs forwarded to engines."""
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> Response:
        """HTTP POST with fallback chain; url target, kwargs forwarded to engines."""
        return self.request("POST", url, **kwargs)

    def request(self, method: str, url: str, **kwargs: Any) -> Response:
        """HTTP request with fallback chain; returns Scraplex Response."""
        headers = kwargs.pop("headers", None)
        params = kwargs.pop("params", None)
        data = kwargs.pop("data", None)
        json_body = kwargs.pop("json", None)
        timeout = kwargs.pop("timeout", None)

        chain = resolve_fallback_chain(
            use_default=self._fallback_use_default,
            explicit=self._fallback_explicit,
            installed=installed_engine_ids(),
        )
        if not chain:
            raise EngineUnavailable("any", "no engines installed; see README.md")

        merged_headers = self._state.merge_headers(headers)
        attempts: list[str] = []
        last_response: Response | None = None

        for engine_id in chain:
            attempts.append(engine_id)
            engine = create_engine(engine_id)
            response = engine.request(
                method,
                url,
                headers=merged_headers,
                cookies=dict(self._state.cookies),
                params=params,
                data=data,
                json=json_body,
                timeout=timeout,
                **kwargs,
            )
            self._state.cookies.update(response.cookies)
            last_response = Response(
                status_code=response.status_code,
                headers=response.headers,
                content=response.content,
                text=response.text,
                url=response.url,
                cookies=response.cookies,
                engine=response.engine,
                handle=response.handle,
                attempts=tuple(attempts),
            )
            if not should_escalate(last_response):
                return last_response

        if last_response is not None:
            return last_response
        raise EscalationExhausted(url, attempts)
