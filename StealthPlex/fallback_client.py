from __future__ import annotations

import logging
from typing import Any

from StealthPlex.engines.registry import create_engine, installed_engine_ids
from StealthPlex.exceptions import EscalationExhausted, EngineUnavailable
from StealthPlex.fallback import resolve_fallback_chain, should_escalate
from StealthPlex.response import Response
from StealthPlex.session import Session
from StealthPlex.types import EngineId

log = logging.getLogger("StealthPlex")


class FallbackClient:
    """Stealth multi-engine fallback — the default mode of StealthPlex.

    Each engine uses its **own** built-in stealth:
      - curl_cffi: libcurl JA3/JA4 Chrome impersonation
      - wreq: Rust-level TLS/HTTP2 Chrome emulation
      - cloudscraper: Cloudflare JS challenge solver
      - scrapling: Playwright-based stealth browser (headed/Xvfb)
      - seleniumbase: Undetected ChromeDriver + CDP mode (headed/Xvfb)

    Usage::

        from StealthPlex import Fetch

        fetch = Fetch()
        resp = fetch.get("https://protected-site.com")
        print(resp.text)       # HTML
        print(resp.json())     # JSON
        print(resp.engine)     # which engine bypassed
    """

    def __init__(
        self,
        *,
        fallback: list[EngineId] | None = None,
    ) -> None:
        """Init stealth fallback client; None = DEFAULT_FALLBACK order."""
        self._state = Session()
        self._fallback_explicit = fallback

    # ------------------------------------------------------------------
    # HTTP methods with full IDE autocomplete signatures
    # ------------------------------------------------------------------

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
        """HTTP GET with stealth fallback chain."""
        return self.request(
            "GET", url, headers=headers, cookies=cookies, params=params,
            timeout=timeout, allow_redirects=allow_redirects,
            redirect=redirect, stream=stream, **kwargs,
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
        """HTTP POST with stealth fallback chain."""
        return self.request(
            "POST", url, headers=headers, cookies=cookies, params=params,
            data=data, json=json, timeout=timeout,
            allow_redirects=allow_redirects, redirect=redirect,
            stream=stream, **kwargs,
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
        """HTTP PUT with stealth fallback chain."""
        return self.request(
            "PUT", url, headers=headers, cookies=cookies, params=params,
            data=data, json=json, timeout=timeout,
            allow_redirects=allow_redirects, redirect=redirect,
            stream=stream, **kwargs,
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
        """HTTP DELETE with stealth fallback chain."""
        return self.request(
            "DELETE", url, headers=headers, cookies=cookies, params=params,
            timeout=timeout, allow_redirects=allow_redirects,
            redirect=redirect, **kwargs,
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
        """HTTP HEAD with stealth fallback chain."""
        return self.request(
            "HEAD", url, headers=headers, cookies=cookies, params=params,
            timeout=timeout, allow_redirects=allow_redirects,
            redirect=redirect, **kwargs,
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
        """HTTP OPTIONS with stealth fallback chain."""
        return self.request(
            "OPTIONS", url, headers=headers, cookies=cookies, params=params,
            timeout=timeout, allow_redirects=allow_redirects,
            redirect=redirect, **kwargs,
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
        """HTTP PATCH with stealth fallback chain."""
        return self.request(
            "PATCH", url, headers=headers, cookies=cookies, params=params,
            data=data, json=json, timeout=timeout,
            allow_redirects=allow_redirects, redirect=redirect,
            stream=stream, **kwargs,
        )

    # ------------------------------------------------------------------
    # Core request dispatcher — each engine uses its OWN stealth
    # ------------------------------------------------------------------

    def request(self, method: str, url: str, **kwargs: Any) -> Response:
        """Stealth HTTP request — engines handle fingerprinting internally."""
        headers = kwargs.pop("headers", None)
        params = kwargs.pop("params", None)
        data = kwargs.pop("data", None)
        json_body = kwargs.pop("json", None)
        timeout = kwargs.pop("timeout", None)
        cookies = kwargs.pop("cookies", None)

        allow_redirects = kwargs.pop("allow_redirects", None)
        if allow_redirects is None:
            allow_redirects = kwargs.pop("redirect", None)
        else:
            kwargs.pop("redirect", None)

        stream = kwargs.pop("stream", None)

        # User headers are passed through — each engine adds its own
        # stealth headers (User-Agent, Sec-CH-UA, TLS fingerprint, etc.)
        merged_headers = self._state.merge_headers(headers)

        merged_cookies = dict(self._state.cookies)
        if cookies:
            merged_cookies.update(cookies)

        # Resolve chain
        use_default = self._fallback_explicit is None
        chain = resolve_fallback_chain(
            use_default=use_default,
            explicit=self._fallback_explicit,
            installed=installed_engine_ids(),
        )
        if not chain:
            raise EngineUnavailable(
                "any", "no engines installed; run: uv sync --extra all"
            )

        attempts: list[str] = []
        last_response: Response | None = None

        for engine_id in chain:
            attempts.append(engine_id)

            try:
                engine = create_engine(engine_id)
            except (EngineUnavailable, Exception) as exc:
                log.debug("skip %s: %s", engine_id, exc)
                continue

            engine_kwargs = dict(kwargs)
            if allow_redirects is not None:
                engine_kwargs["allow_redirects"] = allow_redirects
            if stream is not None:
                engine_kwargs["stream"] = stream

            try:
                raw = engine.request(
                    method, url,
                    headers=merged_headers or None,
                    cookies=merged_cookies or None,
                    params=params,
                    data=data,
                    json=json_body,
                    timeout=timeout,
                    **engine_kwargs,
                )
            except Exception as exc:
                log.debug("%s raised %s — escalating", engine_id, exc)
                continue

            self._state.cookies.update(raw.cookies)
            last_response = Response(
                status_code=raw.status_code,
                headers=raw.headers,
                content=raw.content,
                text=raw.text,
                url=raw.url,
                cookies=raw.cookies,
                engine=raw.engine,
                handle=raw.handle,
                attempts=tuple(attempts),
            )

            if not should_escalate(last_response):
                log.debug("bypass OK via %s (status=%d)",
                          engine_id, last_response.status_code)
                return last_response
            log.debug("%s blocked (status=%d) — escalating",
                      engine_id, last_response.status_code)

        if last_response is not None:
            return last_response
        raise EscalationExhausted(url, attempts)
