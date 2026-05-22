from __future__ import annotations

from types import ModuleType
from typing import Any

from StealthPlex.engines.curl_cffi._docs import (
    ASYNC_HTTP_KWARGS,
    HTTP_KWARGS,
    PROXY_CLASS,
    REQUEST_KWARGS,
)
from StealthPlex.types import EngineId

_SKIP = frozenset({"get", "post", "put", "patch", "delete", "head", "options", "request"})


def _pkg() -> ModuleType:
    import curl_cffi

    return curl_cffi


def _req() -> ModuleType:
    import curl_cffi.requests

    return curl_cffi.requests


class _CurlCffiAsyncAPI:
    """One-shot async HTTP via ``AsyncSession`` (like ``curl_cffi.requests`` sync shortcuts)."""

    def __init__(self, proxy: CurlCffiProxy) -> None:
        object.__setattr__(self, "_proxy", proxy)

    def _session_cls(self) -> type:
        return object.__getattribute__(self, "_proxy").AsyncSession

    async def _call(self, name: str, *args: Any, **kwargs: Any) -> Any:
        session_cls = self._session_cls()
        async with session_cls() as session:
            method = getattr(session, name)
            return await method(*args, **kwargs)

    async def get(self, url: str, **kwargs: Any) -> Any:
        """HTTP GET async (AsyncSession one-shot).""" + ASYNC_HTTP_KWARGS
        return await self._call("get", url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> Any:
        """HTTP POST async (AsyncSession one-shot).""" + ASYNC_HTTP_KWARGS
        return await self._call("post", url, **kwargs)

    async def put(self, url: str, **kwargs: Any) -> Any:
        """HTTP PUT async (AsyncSession one-shot).""" + ASYNC_HTTP_KWARGS
        return await self._call("put", url, **kwargs)

    async def patch(self, url: str, **kwargs: Any) -> Any:
        """HTTP PATCH async (AsyncSession one-shot).""" + ASYNC_HTTP_KWARGS
        return await self._call("patch", url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> Any:
        """HTTP DELETE async (AsyncSession one-shot).""" + ASYNC_HTTP_KWARGS
        return await self._call("delete", url, **kwargs)

    async def head(self, url: str, **kwargs: Any) -> Any:
        """HTTP HEAD async (AsyncSession one-shot).""" + ASYNC_HTTP_KWARGS
        return await self._call("head", url, **kwargs)

    async def options(self, url: str, **kwargs: Any) -> Any:
        """HTTP OPTIONS async (AsyncSession one-shot).""" + ASYNC_HTTP_KWARGS
        return await self._call("options", url, **kwargs)

    async def trace(self, url: str, **kwargs: Any) -> Any:
        """HTTP TRACE async (AsyncSession one-shot).""" + ASYNC_HTTP_KWARGS
        return await self._call("trace", url, **kwargs)

    async def query(self, url: str, **kwargs: Any) -> Any:
        """HTTP QUERY async (AsyncSession one-shot).""" + ASYNC_HTTP_KWARGS
        return await self._call("query", url, **kwargs)

    async def request(self, method: str, url: str, **kwargs: Any) -> Any:
        """HTTP request async (AsyncSession one-shot).""" + REQUEST_KWARGS
        return await self._call("request", method, url, **kwargs)


class CurlCffiProxy:
    __doc__ = PROXY_CLASS

    def __init__(self) -> None:
        """Bind curl_cffi API; requires StealthPlex[curl_cffi]."""
        mod, req = _pkg(), _req()
        object.__setattr__(self, "_module", mod)
        object.__setattr__(self, "_requests", req)
        for name in mod.__all__:
            if name not in _SKIP and hasattr(mod, name):
                object.__setattr__(self, name, getattr(mod, name))
        for name in ("trace", "query"):
            if hasattr(req, name):
                object.__setattr__(self, name, getattr(req, name))
        object.__setattr__(self, "requests", req)
        object.__setattr__(self, "aio", _CurlCffiAsyncAPI(self))

    def _call(self, name: str, *args: Any, **kwargs: Any) -> Any:
        mod = object.__getattribute__(self, "_module")
        if hasattr(mod, name):
            return getattr(mod, name)(*args, **kwargs)
        return getattr(object.__getattribute__(self, "_requests"), name)(*args, **kwargs)

    def get(self, url: str, **kwargs: Any) -> Any:
        """HTTP GET (curl_cffi.get).""" + HTTP_KWARGS
        return self._call("get", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> Any:
        """HTTP POST (curl_cffi.post).""" + HTTP_KWARGS
        return self._call("post", url, **kwargs)

    def put(self, url: str, **kwargs: Any) -> Any:
        """HTTP PUT (curl_cffi.put).""" + HTTP_KWARGS
        return self._call("put", url, **kwargs)

    def patch(self, url: str, **kwargs: Any) -> Any:
        """HTTP PATCH (curl_cffi.patch).""" + HTTP_KWARGS
        return self._call("patch", url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> Any:
        """HTTP DELETE (curl_cffi.delete).""" + HTTP_KWARGS
        return self._call("delete", url, **kwargs)

    def head(self, url: str, **kwargs: Any) -> Any:
        """HTTP HEAD (curl_cffi.head).""" + HTTP_KWARGS
        return self._call("head", url, **kwargs)

    def options(self, url: str, **kwargs: Any) -> Any:
        """HTTP OPTIONS (curl_cffi.options).""" + HTTP_KWARGS
        return self._call("options", url, **kwargs)

    def trace(self, url: str, **kwargs: Any) -> Any:
        """HTTP TRACE (curl_cffi.requests.trace).""" + HTTP_KWARGS
        return self._call("trace", url, **kwargs)

    def query(self, url: str, **kwargs: Any) -> Any:
        """HTTP QUERY (curl_cffi.requests.query).""" + HTTP_KWARGS
        return self._call("query", url, **kwargs)

    def request(self, method: str, url: str, **kwargs: Any) -> Any:
        """HTTP request (curl_cffi.request).""" + REQUEST_KWARGS
        return self._call("request", method, url, **kwargs)

    def __getattr__(self, name: str) -> Any:
        mod = object.__getattribute__(self, "_module")
        if hasattr(mod, name):
            return getattr(mod, name)
        return getattr(object.__getattribute__(self, "_requests"), name)

    @property
    def id(self) -> EngineId:
        return "curl_cffi"

    def installed(self) -> bool:
        try:
            _pkg()
            return True
        except ImportError:
            return False
