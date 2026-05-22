from __future__ import annotations

from typing import Any

from StealthPlex.engines.registry import create_engine, installed_engine_ids
from StealthPlex.exceptions import EscalationExhausted, EngineUnavailable
from StealthPlex.fallback import resolve_fallback_chain, should_escalate
from StealthPlex.response import Response
from StealthPlex.session import Session
from StealthPlex.types import EngineId

FALLBACK_DOC = """Multi-engine fallback — returns StealthPlex ``Response``.

Tries engines in order (``fallback=True`` uses DEFAULT_FALLBACK: wreq → curl_cffi →
cloudscraper → scrapling → seleniumbase).

Returns StealthPlex ``Response`` with ``.engine``, ``.attempts``, ``.handle``.

Example:
    fetch = Fetch(fallback=True)
    r = fetch.get("https://example.com")
"""


class FallbackClient:
    """Multi-engine fallback; get/post/request return StealthPlex Response."""

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

    def get(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        redirect: bool | None = None,
        stream: bool | None = None,
        **kwargs: Any,
    ) -> Response:
        """HTTP GET with fallback chain; returns StealthPlex Response."""
        return self.request(
            "GET",
            url,
            headers=headers,
            cookies=cookies,
            params=params,
            timeout=timeout,
            allow_redirects=allow_redirects,
            redirect=redirect,
            stream=stream,
            **kwargs,
        )

    def post(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        redirect: bool | None = None,
        stream: bool | None = None,
        **kwargs: Any,
    ) -> Response:
        """HTTP POST with fallback chain; returns StealthPlex Response."""
        return self.request(
            "POST",
            url,
            headers=headers,
            cookies=cookies,
            params=params,
            data=data,
            json=json,
            timeout=timeout,
            allow_redirects=allow_redirects,
            redirect=redirect,
            stream=stream,
            **kwargs,
        )

    def put(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        redirect: bool | None = None,
        stream: bool | None = None,
        **kwargs: Any,
    ) -> Response:
        """HTTP PUT with fallback chain; returns StealthPlex Response."""
        return self.request(
            "PUT",
            url,
            headers=headers,
            cookies=cookies,
            params=params,
            data=data,
            json=json,
            timeout=timeout,
            allow_redirects=allow_redirects,
            redirect=redirect,
            stream=stream,
            **kwargs,
        )

    def delete(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        redirect: bool | None = None,
        **kwargs: Any,
    ) -> Response:
        """HTTP DELETE with fallback chain; returns StealthPlex Response."""
        return self.request(
            "DELETE",
            url,
            headers=headers,
            cookies=cookies,
            params=params,
            timeout=timeout,
            allow_redirects=allow_redirects,
            redirect=redirect,
            **kwargs,
        )

    def head(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        redirect: bool | None = None,
        **kwargs: Any,
    ) -> Response:
        """HTTP HEAD with fallback chain; returns StealthPlex Response."""
        return self.request(
            "HEAD",
            url,
            headers=headers,
            cookies=cookies,
            params=params,
            timeout=timeout,
            allow_redirects=allow_redirects,
            redirect=redirect,
            **kwargs,
        )

    def options(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        redirect: bool | None = None,
        **kwargs: Any,
    ) -> Response:
        """HTTP OPTIONS with fallback chain; returns StealthPlex Response."""
        return self.request(
            "OPTIONS",
            url,
            headers=headers,
            cookies=cookies,
            params=params,
            timeout=timeout,
            allow_redirects=allow_redirects,
            redirect=redirect,
            **kwargs,
        )

    def patch(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        redirect: bool | None = None,
        stream: bool | None = None,
        **kwargs: Any,
    ) -> Response:
        """HTTP PATCH with fallback chain; returns StealthPlex Response."""
        return self.request(
            "PATCH",
            url,
            headers=headers,
            cookies=cookies,
            params=params,
            data=data,
            json=json,
            timeout=timeout,
            allow_redirects=allow_redirects,
            redirect=redirect,
            stream=stream,
            **kwargs,
        )

    def request(self, method: str, url: str, **kwargs: Any) -> Response:
        """HTTP request with fallback chain; returns StealthPlex Response."""
        headers = kwargs.pop("headers", None)
        params = kwargs.pop("params", None)
        data = kwargs.pop("data", None)
        json_body = kwargs.pop("json", None)
        timeout = kwargs.pop("timeout", None)
        cookies = kwargs.pop("cookies", None)

        allow_redirects = kwargs.pop("allow_redirects", None)
        if allow_redirects is None:
            allow_redirects = kwargs.pop("redirect", None)

        stream = kwargs.pop("stream", None)

        chain = resolve_fallback_chain(
            use_default=self._fallback_use_default,
            explicit=self._fallback_explicit,
            installed=installed_engine_ids(),
        )
        if not chain:
            raise EngineUnavailable("any", "no engines installed; see README.md")

        merged_headers = self._state.merge_headers(headers)
        
        merged_cookies = dict(self._state.cookies)
        if cookies:
            merged_cookies.update(cookies)

        attempts: list[str] = []
        last_response: Response | None = None

        for engine_id in chain:
            attempts.append(engine_id)
            engine = create_engine(engine_id)
            
            engine_kwargs = dict(kwargs)
            if allow_redirects is not None:
                engine_kwargs["allow_redirects"] = allow_redirects
            if stream is not None:
                engine_kwargs["stream"] = stream

            response = engine.request(
                method,
                url,
                headers=merged_headers,
                cookies=merged_cookies,
                params=params,
                data=data,
                json=json_body,
                timeout=timeout,
                **engine_kwargs,
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
