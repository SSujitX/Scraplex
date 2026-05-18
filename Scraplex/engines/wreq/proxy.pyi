"""IDE stubs: mirror wreq public API (install wreq in active venv). https://github.com/0x676e67/wreq-python"""

from types import ModuleType
from typing import Any, Unpack

import wreq.blocking as blocking
from wreq import (
    Action,
    AlpnProtocol,
    AlpsProtocol,
    Attempt,
    BodyError,
    BuilderError,
    CertStore,
    CertificateCompressionAlgorithm,
    ConnectionError,
    ConnectionResetError,
    Cookie,
    DecodingError,
    Emulation,
    ExtensionType,
    HeaderMap,
    History,
    Http1Options,
    Http2Options,
    Identity,
    Jar,
    KeyLog,
    KeyShare,
    LookupIpStrategy,
    OrigHeaderMap,
    Platform,
    Policy,
    Priorities,
    Priority,
    Profile,
    Proxy,
    ProxyConnectionError,
    PseudoId,
    PseudoOrder,
    RedirectError,
    RequestError,
    ResolverOptions,
    RustPanic,
    SettingId,
    SettingsOrder,
    StatusError,
    TimeoutError,
    TlsError,
    TlsInfo,
    TlsOptions,
    TlsVersion,
    UpgradeError,
    WebSocketError,
)
from wreq import Client, Message, Method, Multipart, Part, Response, SocketAddr, StatusCode, Streamer, Version, WebSocket
from wreq.wreq import ClientConfig, Request, WebSocketRequest


class WreqProxy:
    """wreq — Async HTTP client with TLS/JA3/JA4 fingerprint (same as ``import wreq``).

    Use ``await fetch.get(...)``, ``fetch.Client(...)``, ``fetch.Emulation``, ``fetch.blocking.Client`` for sync.
    Returns wreq ``Response`` (``response.status``, ``await response.text()``, ``await response.json()``).

    Docs & use cases: https://github.com/0x676e67/wreq-python

    Examples:
        import asyncio
        from Scraplex import Fetch
        fetch = Fetch(engine="wreq")
        async def main():
            r = await fetch.get("https://example.com", emulation=fetch.Emulation.Firefox149)
            print(await r.text())
        asyncio.run(main())
    """

    Client: type[Client]
    Method: type[Method]
    Message: type[Message]
    Response: type[Response]
    WebSocket: type[WebSocket]
    Version: type[Version]
    StatusCode: type[StatusCode]
    Multipart: type[Multipart]
    Part: type[Part]
    Streamer: type[Streamer]
    SocketAddr: type[SocketAddr]
    Emulation: type[Emulation]
    Profile: type[Profile]
    Platform: type[Platform]
    HeaderMap: type[HeaderMap]
    OrigHeaderMap: type[OrigHeaderMap]
    Jar: type[Jar]
    Cookie: type[Cookie]
    Proxy: type[Proxy]
    blocking: ModuleType

    async def get(self, url: str, **kwargs: Unpack[Request]) -> Response:
        """HTTP GET (wreq.get).

        Args:
            url: Target URL.
            emulation: Browser/device profile (``Emulation.Firefox149``, ...).
            headers: Request headers.
            json: JSON body.
            timeout: ``datetime.timedelta`` timeout.
            proxies: Proxy list.

        Returns:
            wreq Response — ``await response.text()``, ``response.status``, ``await response.json()``.
        """
        ...

    async def post(self, url: str, **kwargs: Unpack[Request]) -> Response:
        """HTTP POST (wreq.post); kwargs: json, data, multipart, emulation, headers, ..."""
        ...

    async def put(self, url: str, **kwargs: Unpack[Request]) -> Response:
        """HTTP PUT (wreq.put); kwargs: json, data, emulation, headers, ..."""
        ...

    async def patch(self, url: str, **kwargs: Unpack[Request]) -> Response:
        """HTTP PATCH (wreq.patch); kwargs: json, data, emulation, headers, ..."""
        ...

    async def delete(self, url: str, **kwargs: Unpack[Request]) -> Response:
        """HTTP DELETE (wreq.delete); kwargs: emulation, headers, ..."""
        ...

    async def head(self, url: str, **kwargs: Unpack[Request]) -> Response:
        """HTTP HEAD (wreq.head); kwargs: emulation, headers, ..."""
        ...

    async def options(self, url: str, **kwargs: Unpack[Request]) -> Response:
        """HTTP OPTIONS (wreq.options); kwargs: emulation, headers, ..."""
        ...

    async def trace(self, url: str, **kwargs: Unpack[Request]) -> Response:
        """HTTP TRACE (wreq.trace); kwargs: emulation, headers, ..."""
        ...

    async def request(self, method: Method, url: str, **kwargs: Unpack[Request]) -> Response:
        """HTTP request (wreq.request); method, url, emulation, headers, json, ..."""
        ...

    async def websocket(self, url: str, **kwargs: Unpack[WebSocketRequest]) -> WebSocket:
        """WebSocket upgrade (wreq.websocket)."""
        ...

    def __init__(self) -> None:
        """Create proxy; requires Scraplex[wreq] installed."""
        ...

    def __getattr__(self, name: str) -> Any: ...

    @property
    def id(self) -> str: ...

    def installed(self) -> bool: ...
