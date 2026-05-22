from __future__ import annotations

from typing import Any

from StealthPlex.response import Response
from StealthPlex.types import EngineId


def _sb_factory() -> Any:
    from seleniumbase import SB

    return SB


def _normalize_cookies(driver: Any) -> dict[str, str]:
    if driver is None:
        return {}
    try:
        return {str(c["name"]): str(c["value"]) for c in driver.get_cookies()}
    except (AttributeError, KeyError, TypeError):
        return {}
    return {}


class SeleniumBaseEngine:
    """seleniumbase engine adapter; UC+CDP via SB.activate_cdp_mode for fallback chain."""

    def __init__(self) -> None:
        self._kwargs: dict[str, Any] = {"uc": True, "headless": True, "test": True}

    @property
    def id(self) -> EngineId:
        return "seleniumbase"

    def installed(self) -> bool:
        try:
            _sb_factory()
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
        """Fetch URL via UC+CDP (activate_cdp_mode); returns page HTML as StealthPlex Response."""
        del headers, cookies, data, json  # CDP path does not apply HTTP client kwargs
        if method.upper() not in ("GET", "HEAD"):
            raise NotImplementedError("seleniumbase fallback supports GET/HEAD only")
        
        clean_kwargs = dict(kwargs)
        clean_kwargs.pop("allow_redirects", None)
        clean_kwargs.pop("redirect", None)
        clean_kwargs.pop("stream", None)

        sb_kwargs = {**self._kwargs, **clean_kwargs}
        target = url
        if params:
            from urllib.parse import urlencode, urlparse, urlunparse

            parsed = urlparse(url)
            query = urlencode(params)
            sep = "&" if parsed.query else ""
            new_query = f"{parsed.query}{sep}{query}" if parsed.query else query
            target = urlunparse(parsed._replace(query=new_query))

        with _sb_factory()(**sb_kwargs) as sb:
            sb.activate_cdp_mode(target)
            if timeout is not None:
                sb.sleep(min(timeout, 30.0))
            else:
                sb.sleep(1.0)
            text = sb.get_page_source()
            final_url = sb.get_current_url()
            cookie_jar = _normalize_cookies(getattr(sb, "driver", None))

        content = text.encode("utf-8", errors="replace")
        return Response(
            status_code=200,
            headers={},
            content=content,
            text=text,
            url=final_url,
            cookies=cookie_jar,
            engine=self.id,
            handle=None,
            attempts=(self.id,),
        )
