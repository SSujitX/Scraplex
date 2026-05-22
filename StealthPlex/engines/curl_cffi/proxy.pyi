"""
IDE stubs: mirror curl_cffi public API (install curl-cffi in active venv).
https://github.com/lexiforest/curl_cffi
"""

from types import ModuleType
from typing import Any, Unpack

from curl_cffi import (
    AsyncCurl,
    AsyncSession,
    AsyncWebSocket,
    BrowserType,
    BrowserTypeLiteral,
    CookieTypes,
    Cookies,
    Curl,
    CurlECode,
    CurlError,
    CurlFollow,
    CurlHttpVersion,
    CurlInfo,
    CurlMime,
    CurlMOpt,
    CurlOpt,
    CurlSslVersion,
    CurlWsFlag,
    ExtraFingerprints,
    HeaderTypes,
    Headers,
    ProxySpec,
    Request,
    Response,
    Session,
    WebSocket,
    WebSocketClosed,
    WebSocketError,
    WebSocketRetryStrategy,
    WebSocketTimeout,
    WsCloseCode,
    config_warnings,
    exceptions,
    ffi,
    is_pro,
    lib,
)
from curl_cffi.requests import SessionRequestParams
from curl_cffi.requests.session import HttpMethod, RequestParams, ThreadType

import curl_cffi.requests as requests


class CurlCffiAsyncAPI:
    """Async one-shot HTTP via ``AsyncSession`` — use ``await fetch.aio.get(...)``."""

    async def get(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """HTTP GET async (``AsyncSession`` one-shot); kwargs: impersonate, headers, cookies, ..."""
        ...

    async def post(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """HTTP POST async; kwargs: data, json, impersonate, headers, ..."""
        ...

    async def put(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """HTTP PUT async; kwargs: data, json, impersonate, headers, ..."""
        ...

    async def patch(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """HTTP PATCH async; kwargs: data, json, impersonate, headers, ..."""
        ...

    async def delete(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """HTTP DELETE async; kwargs: impersonate, headers, cookies, ..."""
        ...

    async def head(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """HTTP HEAD async; kwargs: impersonate, headers, ..."""
        ...

    async def options(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """HTTP OPTIONS async; kwargs: impersonate, headers, ..."""
        ...

    async def trace(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """HTTP TRACE async; kwargs: impersonate, headers, ..."""
        ...

    async def query(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """HTTP QUERY async; kwargs: impersonate, headers, ..."""
        ...

    async def request(
        self,
        method: HttpMethod,
        url: str,
        **kwargs: Unpack[RequestParams],
    ) -> Response:
        """HTTP request async; method, url, impersonate, headers, cookies, ..."""
        ...


class CurlCffiProxy:
    """curl_cffi — Same API as ``import curl_cffi`` (sync + async, TLS/JA3, HTTP/2/3).

    Sync: ``fetch.get(...)``, ``fetch.Session(...)``.
    Async: ``await fetch.aio.get(...)``, ``fetch.AsyncSession(...)``.

    Docs & use cases: https://github.com/lexiforest/curl_cffi

    Examples:
        from StealthPlex import Fetch
        fetch = Fetch(engine="curl_cffi")
        r = fetch.get("https://example.com", impersonate="chrome")
        async with fetch.AsyncSession(impersonate="chrome124") as s:
            r = await s.get("https://example.com")
        r = await fetch.aio.get("https://example.com", impersonate="chrome")
    """

    aio: CurlCffiAsyncAPI

    # curl_cffi.__all__ surface (bound at runtime from upstream module)
    Session: type[Session]
    AsyncSession: type[AsyncSession]
    WebSocket: type[WebSocket]
    AsyncWebSocket: type[AsyncWebSocket]
    Response: type[Response]
    Request: type[Request]
    Cookies: type[Cookies]
    Headers: type[Headers]
    BrowserType: type[BrowserType]
    BrowserTypeLiteral: type[BrowserTypeLiteral]
    CookieTypes: type[CookieTypes]
    HeaderTypes: type[HeaderTypes]
    ProxySpec: type[ProxySpec]
    ExtraFingerprints: type[ExtraFingerprints]
    Curl: type[Curl]
    AsyncCurl: type[AsyncCurl]
    CurlMime: type[CurlMime]
    CurlError: type[CurlError]
    CurlInfo: type[CurlInfo]
    CurlOpt: type[CurlOpt]
    CurlMOpt: type[CurlMOpt]
    CurlECode: type[CurlECode]
    CurlHttpVersion: type[CurlHttpVersion]
    CurlFollow: type[CurlFollow]
    CurlSslVersion: type[CurlSslVersion]
    CurlWsFlag: type[CurlWsFlag]
    WebSocketClosed: type[WebSocketClosed]
    WebSocketError: type[WebSocketError]
    WebSocketTimeout: type[WebSocketTimeout]
    WebSocketRetryStrategy: type[WebSocketRetryStrategy]
    WsCloseCode: type[WsCloseCode]
    config_warnings: Any
    ffi: Any
    is_pro: bool
    lib: Any
    exceptions: Any
    requests: ModuleType

    def get(self, url: str, **kwargs: Unpack[SessionRequestParams]) -> Response:
        """HTTP GET (curl_cffi.get).

        Args:
            url: Target URL.
            impersonate: Browser fingerprint (chrome, chrome124, safari, ...).
            headers: Request headers.
            cookies: Cookies to send.
            params: Query string parameters.
            data: Form body or bytes.
            json: JSON body.
            timeout: Timeout in seconds or (connect, read) tuple.
            proxies: Proxy configuration.
            proxy: Single proxy URL.
            ja3: Custom JA3 string.
            akamai: Custom Akamai fingerprint.
            http_version: HTTP version (v2, v3, ...).

        Returns:
            Response with .status_code, .json(), .text, .headers, .cookies.
        """
        ...

    def post(self, url: str, **kwargs: Unpack[SessionRequestParams]) -> Response:
        """HTTP POST (curl_cffi.post); kwargs: data, json, impersonate, headers, cookies, params, timeout, ..."""
        ...

    def put(self, url: str, **kwargs: Unpack[SessionRequestParams]) -> Response:
        """HTTP PUT (curl_cffi.put); kwargs: data, json, impersonate, headers, cookies, ..."""
        ...

    def patch(self, url: str, **kwargs: Unpack[SessionRequestParams]) -> Response:
        """HTTP PATCH (curl_cffi.patch); kwargs: data, json, impersonate, headers, ..."""
        ...

    def delete(self, url: str, **kwargs: Unpack[SessionRequestParams]) -> Response:
        """HTTP DELETE (curl_cffi.delete); kwargs: impersonate, headers, cookies, ..."""
        ...

    def head(self, url: str, **kwargs: Unpack[SessionRequestParams]) -> Response:
        """HTTP HEAD (curl_cffi.head); kwargs: impersonate, headers, cookies, ..."""
        ...

    def options(self, url: str, **kwargs: Unpack[SessionRequestParams]) -> Response:
        """HTTP OPTIONS (curl_cffi.options); kwargs: impersonate, headers, ..."""
        ...

    def trace(self, url: str, **kwargs: Unpack[SessionRequestParams]) -> Response:
        """HTTP TRACE (curl_cffi.requests.trace); kwargs: impersonate, headers, ..."""
        ...

    def query(self, url: str, **kwargs: Unpack[SessionRequestParams]) -> Response:
        """HTTP QUERY (curl_cffi.requests.query); kwargs: impersonate, headers, ..."""
        ...

    def request(
        self,
        method: HttpMethod,
        url: str,
        thread: ThreadType | None = None,
        curl_options: dict[Any, Any] | None = None,
        debug: bool | None = None,
        **kwargs: Unpack[RequestParams],
    ) -> Response:
        """HTTP request (curl_cffi.request); method, url, impersonate, headers, cookies, params, ..."""
        ...

    def __init__(self) -> None:
        """Create proxy; requires StealthPlex[curl_cffi] installed."""
        ...

    def __getattr__(self, name: str) -> Any: ...

    @property
    def id(self) -> str: ...

    def installed(self) -> bool: ...
