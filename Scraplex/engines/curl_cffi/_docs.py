from Scraplex.engines.docs import ENGINE_INFO, proxy_doc

HTTP_KWARGS = """
Args:
    url: Target URL.
    params: Query string dict.
    headers: Request headers dict.
    cookies: Cookies dict or jar.
    data: Form body or bytes.
    json: JSON body.
    timeout: Seconds or (connect, read) tuple.
    allow_redirects: Follow redirects.
    max_redirects: Max redirects (-1 unlimited).
    proxies: Proxy map for http/https.
    proxy: Single proxy URL.
    proxy_auth: Proxy credentials (user, password).
    verify: Verify TLS certificates.
    referer: Referer header.
    impersonate: Browser fingerprint (chrome, chrome124, safari, ...).
    ja3: Custom JA3 string.
    akamai: Custom Akamai fingerprint.
    extra_fp: Extra fingerprint options.
    http_version: HTTP version (v2, v3).
    stream: Stream response body.
    multipart: Multipart upload.
    auth: HTTP basic auth (user, password).

Returns:
    curl_cffi Response (.status_code, .json(), .text, .headers, .cookies).
"""

ASYNC_HTTP_KWARGS = """
Async one-shot (``AsyncSession``). Same kwargs as sync get().

Returns:
    curl_cffi Response — same as sync (.status_code, .json(), .text, ...).
"""

REQUEST_KWARGS = """
Args:
    method: HTTP verb (GET, POST, PUT, DELETE, HEAD, OPTIONS, TRACE, PATCH, QUERY).
    url: Target URL.
    thread: eventlet or gevent.
    curl_options: Extra libcurl options.
    debug: Print curl debug log.
    (plus all get() parameters: impersonate, headers, cookies, params, timeout, ...).

Returns:
    curl_cffi Response (.status_code, .json(), .text, .headers, .cookies).
"""

CURL_CFFI_GITHUB = ENGINE_INFO["curl_cffi"].github

PROXY_CLASS = f"""
curl_cffi — same API as ``import curl_cffi`` (sync + async).

Sync: ``client.get(...)``, ``client.Session(...)``.
Async: ``await client.aio.get(...)``, ``client.AsyncSession(...)``.

Docs & use cases: {CURL_CFFI_GITHUB}
"""

CLIENT_CURL_CFFI = proxy_doc("curl_cffi")
