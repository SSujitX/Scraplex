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
        raw = driver.get_cookies()
    except Exception:
        return {}
    out: dict[str, str] = {}
    for item in raw:
        try:
            out[str(item["name"])] = str(item["value"])
        except (KeyError, TypeError):
            continue
    return out


def _infer_status_code(*, text: str, url: str) -> int:
    """Best-effort status when the browser stack does not expose HTTP status."""
    u = url.lower()
    if any(p in u for p in ("/sign_in", "/login", "error_code=403")):
        return 403
    lower = text.lower()
    if any(
        m in lower
        for m in (
            "403 forbidden",
            "access denied",
            "cf-browser-verification",
            "just a moment",
            "attention required",
        )
    ):
        return 403
    return 200


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
        """Fetch URL via UC+CDP + optional solve_captcha; GET/HEAD only."""
        if method.upper() not in ("GET", "HEAD"):
            raise NotImplementedError(
                f"seleniumbase is browser-based; {method.upper()} not supported"
            )

        # Clean kwargs that browsers don't understand
        clean_kwargs = dict(kwargs)
        clean_kwargs.pop("allow_redirects", None)
        clean_kwargs.pop("redirect", None)
        clean_kwargs.pop("stream", None)
        solve_captcha = clean_kwargs.pop("solve_captcha", True)

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

        try:
            with _sb_factory()(**sb_kwargs) as sb:
                if cookies:
                    from urllib.parse import urlparse

                    domain = urlparse(target).hostname or ""
                    sb.open("about:blank")
                    for name, value in cookies.items():
                        sb.add_cookie(
                            {"name": name, "value": value, "domain": domain}
                        )

                sb.activate_cdp_mode(target)

                wait_s = 2.0 if timeout is None else min(max(timeout / 3, 1.0), 10.0)
                sb.sleep(wait_s)

                if solve_captcha:
                    try:
                        sb.solve_captcha()
                    except Exception:
                        pass
                    sb.sleep(wait_s)
                elif timeout is not None:
                    sb.sleep(min(max(timeout - wait_s, 0.0), 28.0))

                try:
                    text = sb.get_page_source() or ""
                except Exception as exc:
                    raise RuntimeError(
                        f"seleniumbase get_page_source failed: {exc}"
                    ) from exc
                try:
                    final_url = sb.get_current_url() or target
                except Exception:
                    final_url = target
                cookie_jar = _normalize_cookies(getattr(sb, "driver", None))
        except NotImplementedError:
            raise
        except Exception as exc:
            raise RuntimeError(f"seleniumbase session failed: {exc}") from exc

        content = text.encode("utf-8", errors="replace")
        return Response(
            status_code=_infer_status_code(text=text, url=final_url),
            headers={},
            content=content,
            text=text,
            url=final_url,
            cookies=cookie_jar,
            engine=self.id,
            handle=None,
            attempts=(self.id,),
        )
