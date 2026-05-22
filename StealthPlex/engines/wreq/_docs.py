from StealthPlex.engines.docs import ENGINE_INFO, proxy_doc

HTTP_KWARGS = """
Args:
    url: Target URL.
    emulation: Browser/device profile (``Emulation.Firefox149``, ``Profile``, ...).
    headers: Request headers dict or ``HeaderMap``.
    orig_headers: Original header order list.
    cookies: Cookies for the request.
    params: Query string parameters.
    json: JSON body dict or list.
    data: Form body.
    multipart: ``Multipart`` upload.
    timeout: Request timeout (``datetime.timedelta``).
    proxies: Proxy list (``Sequence[Proxy]``).
    tls_verify: TLS certificate verification.
    redirect: ``redirect.Policy``.
    gzip: Auto-decompress gzip responses.

Returns:
    wreq ``Response`` — use ``await response.text()``, ``response.status``, ``await response.json()``.
"""

REQUEST_KWARGS = """
Args:
    method: HTTP method (``Method.GET``, ``Method.POST``, ...).
    url: Target URL.
    (plus all get() parameters: emulation, headers, json, timeout, proxies, ...).

Returns:
    wreq ``Response`` — use ``await response.text()``, ``response.status``, ``await response.json()``.
"""

PROXY_CLASS = f"""
wreq proxy — same API as ``import wreq`` (async HTTP + TLS fingerprint).

Sync client: ``blocking.Client``. Docs: {ENGINE_INFO["wreq"].github}
"""

CLIENT_WREQ = proxy_doc("wreq")
