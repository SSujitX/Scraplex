"""Run: uv sync --extra curl_cffi && uv run test_curl_cffi.py"""

from Scraplex import Fetch
from rich import print

fetch = Fetch(engine="curl_cffi")

response = fetch.get(url="https://tls.browserleaks.com/json")

session = fetch.Session(impersonate="chrome124")
session.get("https://httpbin.org/cookies/set/foo/bar")
print(session.cookies)
