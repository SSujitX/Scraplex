from __future__ import annotations

import sys
from typing import Any

from StealthPlex.response import Response
from StealthPlex.types import EngineId



def _sb_factory() -> Any:
    """Import seleniumbase SB; raises ImportError when extra is missing."""
    from seleniumbase import SB

    return SB


def _normalize_cookies(driver: Any) -> dict[str, str]:
    """Extract cookie name/value pairs from seleniumbase driver."""
    if driver is None:
        return {}
    try:
        return {str(c["name"]): str(c["value"]) for c in driver.get_cookies()}
    except (AttributeError, KeyError, TypeError):
        return {}


class SeleniumBaseEngine:
    """seleniumbase engine adapter; UC+CDP for StealthPlex fallback chain."""

    def __init__(self) -> None:
        self._kwargs: dict[str, Any] = {
            "uc": True,
            "headless": False,
            "test": True,
        }
        if sys.platform.startswith("linux"):
            self._kwargs["xvfb"] = True


    @property
    def id(self) -> EngineId:
        """Return engine identifier seleniumbase."""
        return "seleniumbase"

    def installed(self) -> bool:
        """Return True when seleniumbase package is installed."""
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
        """Fetch URL via UC+CDP; browser-based — GET only, skipped for other methods."""
        if method.upper() not in ("GET", "HEAD"):
            raise NotImplementedError(
                f"seleniumbase is browser-based; {method.upper()} not supported"
            )

        # Clean kwargs that browsers don't understand
        clean_kwargs = dict(kwargs)
        clean_kwargs.pop("allow_redirects", None)
        clean_kwargs.pop("redirect", None)
        clean_kwargs.pop("stream", None)

        sb_kwargs = {**self._kwargs, **clean_kwargs}

        # Append params to URL
        target = url
        if params:
            from urllib.parse import urlencode, urlparse, urlunparse

            parsed = urlparse(url)
            query = urlencode(params)
            sep = "&" if parsed.query else ""
            new_query = f"{parsed.query}{sep}{query}" if parsed.query else query
            target = urlunparse(parsed._replace(query=new_query))

        with _sb_factory()(**sb_kwargs) as sb:
            # Inject cookies before navigating
            if cookies:
                from urllib.parse import urlparse

                domain = urlparse(target).hostname or ""
                sb.open("about:blank")
                for name, value in cookies.items():
                    sb.add_cookie({"name": name, "value": value, "domain": domain})

            # Navigate with CDP mode (undetected)
            sb.activate_cdp_mode(target)

            # Wait for page to load and JS challenges to resolve
            if timeout is not None:
                sb.sleep(min(timeout, 30.0))
            else:
                sb.sleep(2.0)

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
