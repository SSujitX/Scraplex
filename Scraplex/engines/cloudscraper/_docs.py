from Scraplex.engines.docs import ENGINE_INFO, proxy_doc

CLOUDSCRAPER_GITHUB = ENGINE_INFO["cloudscraper"].github

CREATE_SCRAPER_KWARGS = """
Args:
    debug: Print request/response debug output.
    disableCloudflareV1: Do not attempt Cloudflare v1 (IUAM) challenges.
    delay: Seconds to wait before submitting challenge (default from page).
    interpreter: JS engine — ``native`` (default), ``js2py``, ``nodejs``, ``v8``, ``chakra``.
    browser: ``chrome``, ``firefox``, or filter dict (platform, mobile, desktop, custom).
    captcha: 3rd-party captcha provider dict (``provider``, ``api_key``, ...).
    doubleDown: Retry challenge on failure.
    cipherSuite: TLS cipher suite string or list.
    ecdhCurve: ECDH curve name (default ``prime256v1``).
    source_address: Bind outbound requests to IP or ``(ip, port)``.
    server_hostname: TLS SNI hostname override.
    allow_brotli: Decompress brotli responses (default when brotli installed).
    solveDepth: Max consecutive challenge solves before error.
    sess: Existing ``requests.Session`` to copy cookies/headers from.

Returns:
    ``CloudScraper`` session — use ``.get()``, ``.post()``, ... like Requests.
"""

GET_TOKENS_KWARGS = """
Args:
    url: Site URL protected by Cloudflare.
    (plus ``create_scraper`` options: browser, interpreter, delay, captcha, debug, ...).

Returns:
    Tuple of (cookie dict, user-agent string). Use the same UA for follow-up requests.
"""

PROXY_CLASS = f"""
cloudscraper — same API as ``import cloudscraper`` (Cloudflare bypass via Requests).

Use ``fetch.create_scraper().get(...)``, ``fetch.CloudScraper()``, ``fetch.get_tokens(url)``.

Docs: {CLOUDSCRAPER_GITHUB} · PyPI: https://pypi.org/project/cloudscraper
"""

CLIENT_CLOUDSCRAPER = proxy_doc("cloudscraper")
