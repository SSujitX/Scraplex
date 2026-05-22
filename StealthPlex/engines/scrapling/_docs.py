from StealthPlex.engines.docs import ENGINE_INFO, proxy_doc

STEALTHPLEX_GITHUB = ENGINE_INFO["scrapling"].github

PROXY_CLASS = f"""StealthPlex — Stealth fetcher with headless browser support (Layer 3).

Exposes all StealthPlex imports (Fetcher, StealthyFetcher, FetcherSession, etc.).
Docs: {STEALTHPLEX_GITHUB}
"""

CLIENT_STEALTHPLEX = proxy_doc("scrapling")
