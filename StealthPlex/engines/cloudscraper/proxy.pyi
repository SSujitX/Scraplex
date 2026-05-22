"""IDE stubs: mirror cloudscraper public API (install StealthPlex[cloudscraper] in active venv)."""

from collections.abc import Callable
from types import ModuleType
from typing import Any, Literal, TypedDict, Unpack

from requests import Response, Session
from requests.adapters import HTTPAdapter
from requests_toolbelt.utils import dump

from StealthPlex.engines.cloudscraper._docs import CREATE_SCRAPER_KWARGS, GET_TOKENS_KWARGS

# ---------------------------------------------------------------------------
# cloudscraper types (mirrors cloudscraper package; avoids broken upstream stubs)
# ---------------------------------------------------------------------------


class BrowserOptions(TypedDict, total=False):
    browser: Literal["chrome", "firefox"]
    mobile: bool
    desktop: bool
    platform: Literal["linux", "windows", "darwin", "android", "ios"]
    custom: str


class CaptchaOptions(TypedDict, total=False):
    provider: Literal[
        "2captcha",
        "anticaptcha",
        "capsolver",
        "capmonster",
        "deathbycaptcha",
        "9kw",
        "return_response",
    ]
    api_key: str
    username: str
    password: str
    clientKey: str
    no_proxy: bool
    maxtimeout: int


class CreateScraperKwargs(TypedDict, total=False):
    debug: bool
    disableCloudflareV1: bool
    delay: float | None
    captcha: CaptchaOptions
    doubleDown: bool
    interpreter: Literal["native", "js2py", "nodejs", "v8", "chakra"]
    requestPreHook: Callable[..., tuple[Any, ...]]
    requestPostHook: Callable[..., Any]
    cipherSuite: str | list[str] | None
    ecdhCurve: str
    source_address: str | tuple[str, int] | None
    server_hostname: str | None
    ssl_context: Any
    allow_brotli: bool
    browser: Literal["chrome", "firefox"] | BrowserOptions | None
    solveDepth: int
    sess: Session | None


class GetTokensKwargs(CreateScraperKwargs, total=False):
    proxies: dict[str, str]
    params: dict[str, Any]
    headers: dict[str, str]
    cookies: dict[str, str]
    timeout: float | tuple[float, float]
    allow_redirects: bool


class CipherSuiteAdapter(HTTPAdapter):
    """Custom TLS adapter for browser-like cipher suites."""

    def __init__(
        self,
        *args: Any,
        ssl_context: Any | None = None,
        cipherSuite: str | None = None,
        source_address: str | tuple[str, int] | None = None,
        server_hostname: str | None = None,
        ecdhCurve: str = "prime256v1",
        **kwargs: Any,
    ) -> None: ...


class Cloudflare:
    """Cloudflare challenge handler (internal)."""

    ...


class CloudScraper(Session):
    """Requests-compatible session that solves Cloudflare anti-bot challenges.

    Create via ``fetch.create_scraper()`` or ``fetch.CloudScraper()``.
    HTTP methods (``.get``, ``.post``, ...) match ``requests.Session``.
    """

    debug: bool
    disableCloudflareV1: bool
    delay: float | None
    captcha: dict[str, Any]
    doubleDown: bool
    interpreter: str
    cipherSuite: str | None
    ecdhCurve: str
    allow_brotli: bool
    solveDepth: int

    def __init__(self, *args: Any, **kwargs: Unpack[CreateScraperKwargs]) -> None:
        """Create CloudScraper session; kwargs match ``create_scraper()``."""
        ...

    @classmethod
    def create_scraper(
        cls,
        sess: Session | None = None,
        **kwargs: Unpack[CreateScraperKwargs],
    ) -> CloudScraper:
        """Convenience function for creating a ready-to-go CloudScraper instance."""
        ...

    @classmethod
    def get_tokens(
        cls,
        url: str,
        **kwargs: Unpack[GetTokensKwargs],
    ) -> tuple[dict[str, str], str]:
        """Return Cloudflare cookie dict and User-Agent for the given URL."""
        ...

    @classmethod
    def get_cookie_string(
        cls,
        url: str,
        **kwargs: Unpack[GetTokensKwargs],
    ) -> tuple[str, str]:
        """Return Cookie header value and User-Agent for the given URL."""
        ...

    def perform_request(self, method: str, url: str, *args: Any, **kwargs: Any) -> Response:
        """Low-level request hook (delegates to ``requests.Session.request``)."""
        ...

    # requests.Session HTTP API (explicit for IDE when requests stubs are weak)
    def get(self, url: str, **kwargs: Any) -> Response:
        """HTTP GET — passes through Cloudflare challenge handling when needed."""
        ...

    def post(self, url: str, **kwargs: Any) -> Response:
        """HTTP POST; kwargs: data, json, headers, cookies, timeout, proxies, ..."""
        ...

    def put(self, url: str, **kwargs: Any) -> Response:
        """HTTP PUT; kwargs: data, json, headers, cookies, ..."""
        ...

    def patch(self, url: str, **kwargs: Any) -> Response:
        """HTTP PATCH; kwargs: data, json, headers, ..."""
        ...

    def delete(self, url: str, **kwargs: Any) -> Response:
        """HTTP DELETE; kwargs: headers, cookies, timeout, ..."""
        ...

    def head(self, url: str, **kwargs: Any) -> Response:
        """HTTP HEAD; kwargs: headers, cookies, allow_redirects, ..."""
        ...

    def options(self, url: str, **kwargs: Any) -> Response:
        """HTTP OPTIONS; kwargs: headers, cookies, ..."""
        ...

    def request(self, method: str, url: str, **kwargs: Any) -> Response:
        """HTTP request; method, url, plus standard Requests kwargs."""
        ...


class CloudflareIUAMError(Exception):
    """Cloudflare IUAM parameter extraction failed."""

    ...


class CloudflareLoopProtection(Exception):
    """Too many consecutive Cloudflare challenge solves."""

    ...


class User_Agent:
    """Browser user-agent / cipher suite picker."""

    headers: dict[str, str]
    cipherSuite: str

    def __init__(
        self,
        *,
        allow_brotli: bool = False,
        browser: Literal["chrome", "firefox"] | BrowserOptions | None = None,
    ) -> None: ...


# ---------------------------------------------------------------------------
# StealthPlex proxy — same surface as ``import cloudscraper``
# ---------------------------------------------------------------------------


class CloudscraperProxy:
    """cloudscraper — Cloudflare-aware HTTP client (same as ``import cloudscraper``).

    Use ``fetch.create_scraper().get(...)``, ``fetch.CloudScraper()``, ``fetch.get_tokens(url)``.
    Returns ``requests.Response`` (``.status_code``, ``.json()``, ``.text``, ``.cookies``).

    Docs: https://github.com/VeNoMouS/cloudscraper · PyPI: https://pypi.org/project/cloudscraper

    Examples:
        from StealthPlex import Fetch
        fetch = Fetch(engine="cloudscraper")
        scraper = fetch.create_scraper(browser="chrome")
        r = scraper.get("https://example.com")
        tokens, ua = fetch.get_tokens("https://example.com")
    """

    __version__: str

    def create_scraper(self, **kwargs: Unpack[CreateScraperKwargs]) -> CloudScraper:
        """Create a CloudScraper session (``cloudscraper.create_scraper``).""" + CREATE_SCRAPER_KWARGS

    def session(self, **kwargs: Unpack[CreateScraperKwargs]) -> CloudScraper:
        """Alias for ``create_scraper()``."""
        ...

    def get_tokens(
        self,
        url: str,
        **kwargs: Unpack[GetTokensKwargs],
    ) -> tuple[dict[str, str], str]:
        """Fetch Cloudflare clearance cookies and User-Agent (``cloudscraper.get_tokens``)."""
        + GET_TOKENS_KWARGS

    def get_cookie_string(
        self,
        url: str,
        **kwargs: Unpack[GetTokensKwargs],
    ) -> tuple[str, str]:
        """Cookie header string + User-Agent for manual HTTP clients."""
        + GET_TOKENS_KWARGS

    CloudScraper: type[CloudScraper]
    CipherSuiteAdapter: type[CipherSuiteAdapter]
    Cloudflare: type[Cloudflare]
    CloudflareIUAMError: type[CloudflareIUAMError]
    CloudflareLoopProtection: type[CloudflareLoopProtection]
    User_Agent: type[User_Agent]
    captcha: ModuleType
    cloudflare: ModuleType
    exceptions: ModuleType
    interpreters: ModuleType
    user_agent: ModuleType
    requests: ModuleType
    dump: ModuleType
    HTTPAdapter: type[HTTPAdapter]
    Session: type[Session]

    def __init__(self) -> None:
        """Create proxy; requires ``uv sync --extra cloudscraper`` and that venv in the IDE."""
        ...

    def __getattr__(self, name: str) -> Any: ...

    @property
    def id(self) -> str: ...

    def installed(self) -> bool: ...
