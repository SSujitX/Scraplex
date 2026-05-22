from __future__ import annotations

from typing import TYPE_CHECKING, Any

from Scraplex.response import Response
from Scraplex.types import EngineId

if TYPE_CHECKING:
    from scrapling.engines.toolbelt.custom import Response as ScraplingResponse


def _import_stealthy_fetcher() -> Any:
    """Import scrapling StealthyFetcher; raises ImportError when extra is missing."""
    from scrapling.fetchers import StealthyFetcher

    return StealthyFetcher


def _ensure_dependencies() -> None:
    """Run scrapling browser install if not already installed."""
    try:
        import scrapling
        from pathlib import Path

        pkg_dir = Path(scrapling.__file__).parent
        marker = pkg_dir / ".scrapling_dependencies_installed"
        if not marker.exists():
            from scrapling.cli import install

            install.callback(force=False)
    except Exception:
        pass



def _normalize_headers(headers: Any) -> dict[str, str]:
    """Convert headers mapping to plain str dict."""
    if headers is None:
        return {}
    if hasattr(headers, "items"):
        return {str(k): str(v) for k, v in headers.items()}
    return {}


def _normalize_cookies(cookies: Any) -> dict[str, str]:
    """Extract and flatten cookie name/value pairs from various formats."""
    if not cookies:
        return {}
    if isinstance(cookies, dict):
        return {str(k): str(v) for k, v in cookies.items()}
    if isinstance(cookies, (list, tuple)):
        normalized: dict[str, str] = {}
        for item in cookies:
            if isinstance(item, dict):
                if "name" in item and "value" in item:
                    normalized[str(item["name"])] = str(item["value"])
                else:
                    for k, v in item.items():
                        normalized[str(k)] = str(v)
        return normalized
    return {}


def response_from_scrapling(
    upstream: ScraplingResponse,
    *,
    engine: EngineId = "scrapling",
    attempts: tuple[str, ...] = (),
) -> Response:
    """Build Scraplex Response from Scrapling Response."""
    content: bytes = upstream.body or b""
    encoding: str = getattr(upstream, "encoding", None) or "utf-8"
    try:
        text = content.decode(encoding, errors="replace")
    except Exception:
        text = ""
    return Response(
        status_code=int(upstream.status),
        headers=_normalize_headers(upstream.headers),
        content=content,
        text=text,
        url=str(upstream.url),
        cookies=_normalize_cookies(upstream.cookies),
        engine=engine,
        handle=upstream,
        attempts=attempts,
    )


class ScraplingEngine:
    """scrapling engine adapter using StealthyFetcher for Scraplex fallback chain."""

    @property
    def id(self) -> EngineId:
        """Return engine identifier scrapling."""
        return "scrapling"

    def installed(self) -> bool:
        """Return True when scrapling package is installed."""
        try:
            _import_stealthy_fetcher()
            return True
        except ImportError:
            return False

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
        """Perform HTTP request via scrapling.StealthyFetcher."""
        if method.upper() not in ("GET", "HEAD"):
            raise NotImplementedError("scrapling fallback engine supports GET/HEAD requests only")

        _ensure_dependencies()
        stealthy_fetcher = _import_stealthy_fetcher()
        target = url
        if params:
            from urllib.parse import urlencode, urlparse, urlunparse

            parsed = urlparse(url)
            query = urlencode(params)
            sep = "&" if parsed.query else ""
            new_query = f"{parsed.query}{sep}{query}" if parsed.query else query
            target = urlunparse(parsed._replace(query=new_query))

        fetch_kwargs: dict[str, Any] = dict(kwargs)
        if headers is not None:
            fetch_kwargs["extra_headers"] = headers
        if cookies is not None:
            fetch_kwargs["cookies"] = [
                {"name": str(k), "value": str(v), "url": target} for k, v in cookies.items()
            ]
        if timeout is not None:
            fetch_kwargs["timeout"] = int(timeout * 1000)

        upstream = stealthy_fetcher.fetch(target, **fetch_kwargs)
        return response_from_scrapling(upstream, attempts=(self.id,))
