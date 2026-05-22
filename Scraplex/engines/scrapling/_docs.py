from Scraplex.engines.docs import ENGINE_INFO, proxy_doc

SCRAPLING_GITHUB = ENGINE_INFO["scrapling"].github

PROXY_CLASS = f"""scrapling — Stealth fetcher with headless browser support (Layer 3).

Exposes all scrapling imports (Fetcher, StealthyFetcher, FetcherSession, etc.).
Docs: {SCRAPLING_GITHUB}
"""

CLIENT_SCRAPLING = proxy_doc("scrapling")
