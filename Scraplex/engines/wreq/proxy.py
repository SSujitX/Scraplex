from __future__ import annotations

from types import ModuleType
from typing import Any

from Scraplex.engines.wreq._docs import HTTP_KWARGS, PROXY_CLASS, REQUEST_KWARGS
from Scraplex.types import EngineId

_SKIP = frozenset({
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "head",
    "options",
    "request",
    "trace",
    "websocket",
})

_EXTRA = (
    "Client",
    "Method",
    "Message",
    "Response",
    "WebSocket",
    "Version",
    "StatusCode",
    "Multipart",
    "Part",
    "Streamer",
    "SocketAddr",
)


def _pkg() -> ModuleType:
    import wreq

    return wreq


class WreqProxy:
    __doc__ = PROXY_CLASS

    def __init__(self) -> None:
        """Bind wreq API; requires Scraplex[wreq]."""
        mod = _pkg()
        object.__setattr__(self, "_module", mod)
        for name in mod.__all__:
            if name not in _SKIP and hasattr(mod, name):
                object.__setattr__(self, name, getattr(mod, name))
        for name in _EXTRA:
            if hasattr(mod, name):
                object.__setattr__(self, name, getattr(mod, name))
        for name in _SKIP:
            if hasattr(mod, name):
                object.__setattr__(self, name, getattr(mod, name))
        if hasattr(mod, "blocking"):
            object.__setattr__(self, "blocking", mod.blocking)

    def _call(self, name: str, *args: Any, **kwargs: Any) -> Any:
        return getattr(object.__getattribute__(self, "_module"), name)(*args, **kwargs)

    async def get(self, url: str, **kwargs: Any) -> Any:
        """HTTP GET (wreq.get).""" + HTTP_KWARGS
        return await self._call("get", url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> Any:
        """HTTP POST (wreq.post).""" + HTTP_KWARGS
        return await self._call("post", url, **kwargs)

    async def put(self, url: str, **kwargs: Any) -> Any:
        """HTTP PUT (wreq.put).""" + HTTP_KWARGS
        return await self._call("put", url, **kwargs)

    async def patch(self, url: str, **kwargs: Any) -> Any:
        """HTTP PATCH (wreq.patch).""" + HTTP_KWARGS
        return await self._call("patch", url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> Any:
        """HTTP DELETE (wreq.delete).""" + HTTP_KWARGS
        return await self._call("delete", url, **kwargs)

    async def head(self, url: str, **kwargs: Any) -> Any:
        """HTTP HEAD (wreq.head).""" + HTTP_KWARGS
        return await self._call("head", url, **kwargs)

    async def options(self, url: str, **kwargs: Any) -> Any:
        """HTTP OPTIONS (wreq.options).""" + HTTP_KWARGS
        return await self._call("options", url, **kwargs)

    async def trace(self, url: str, **kwargs: Any) -> Any:
        """HTTP TRACE (wreq.trace).""" + HTTP_KWARGS
        return await self._call("trace", url, **kwargs)

    async def request(self, method: Any, url: str, **kwargs: Any) -> Any:
        """HTTP request (wreq.request).""" + REQUEST_KWARGS
        return await self._call("request", method, url, **kwargs)

    async def websocket(self, url: str, **kwargs: Any) -> Any:
        """WebSocket (wreq.websocket)."""
        return await self._call("websocket", url, **kwargs)

    def __getattr__(self, name: str) -> Any:
        return getattr(object.__getattribute__(self, "_module"), name)

    @property
    def id(self) -> EngineId:
        return "wreq"

    def installed(self) -> bool:
        try:
            _pkg()
            return True
        except ImportError:
            return False
