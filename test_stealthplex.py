"""StealthPlex integration test — stealth fallback with all HTTP methods.

Run: uv run test_stealthplex.py
"""

from __future__ import annotations

from StealthPlex import Fetch


def test_stealth_get() -> None:
    """Fetch() with no args — auto stealth fallback GET."""
    fetch = Fetch()
    resp = fetch.get("https://httpbin.org/get", params={"q": "stealth"})
    print(f"[GET] {resp}")
    print(f"  engine={resp.engine}, attempts={resp.attempts}")
    data = resp.json()
    print(f"  User-Agent: {data['headers'].get('User-Agent', '???')[:60]}...")
    print(f"  args: {data['args']}")
    assert resp.ok
    assert data["args"]["q"] == "stealth"


def test_stealth_post_json() -> None:
    """POST with JSON body through stealth fallback."""
    fetch = Fetch()
    resp = fetch.post(
        "https://httpbin.org/post",
        json={"action": "login", "user": "admin"},
    )
    print(f"\n[POST JSON] {resp}")
    data = resp.json()
    print(f"  server received json: {data['json']}")
    assert resp.ok
    assert data["json"]["action"] == "login"


def test_stealth_put_data() -> None:
    """PUT with raw data body through stealth fallback."""
    fetch = Fetch()
    resp = fetch.put("https://httpbin.org/put", data="update payload")
    print(f"\n[PUT] {resp}")
    data = resp.json()
    print(f"  server received data: {data['data']}")
    assert resp.ok
    assert data["data"] == "update payload"


def test_stealth_patch() -> None:
    """PATCH with JSON through stealth fallback."""
    fetch = Fetch()
    resp = fetch.patch(
        "https://httpbin.org/patch",
        json={"field": "value"},
    )
    print(f"\n[PATCH] {resp}")
    data = resp.json()
    print(f"  server received json: {data['json']}")
    assert resp.ok
    assert data["json"]["field"] == "value"


def test_stealth_delete() -> None:
    """DELETE through stealth fallback."""
    fetch = Fetch()
    resp = fetch.delete("https://httpbin.org/delete")
    print(f"\n[DELETE] {resp}")
    assert resp.ok


def test_stealth_head() -> None:
    """HEAD through stealth fallback."""
    fetch = Fetch()
    resp = fetch.head("https://httpbin.org/get")
    print(f"\n[HEAD] {resp}")
    assert resp.ok


def test_stealth_options() -> None:
    """OPTIONS through stealth fallback."""
    fetch = Fetch()
    resp = fetch.options("https://httpbin.org/get")
    print(f"\n[OPTIONS] {resp}")
    assert resp.ok


def test_stealth_headers_cookies() -> None:
    """Custom headers + cookies through stealth fallback."""
    fetch = Fetch()
    resp = fetch.get(
        "https://httpbin.org/get",
        headers={"X-Custom": "myvalue"},
        cookies={"session": "abc123"},
    )
    print(f"\n[HEADERS+COOKIES] {resp}")
    data = resp.json()
    print(f"  X-Custom: {data['headers'].get('X-Custom')}")
    cookie_h = data["headers"].get("Cookie", "")
    print(f"  Cookie: {cookie_h}")
    assert resp.ok
    assert data["headers"]["X-Custom"] == "myvalue"
    assert "session=abc123" in cookie_h


def test_stealth_redirect_control() -> None:
    """Redirect control through stealth fallback."""
    fetch = Fetch()
    resp = fetch.get(
        "https://httpbin.org/redirect/1",
        allow_redirects=False,
    )
    print(f"\n[REDIRECT allow_redirects=False] {resp}")
    assert 300 <= resp.status_code < 400


def test_stealth_html_parse() -> None:
    """GET HTML page and parse content."""
    fetch = Fetch()
    resp = fetch.get("https://example.com")
    print(f"\n[HTML PARSE] {resp}")
    assert resp.ok
    assert "<h1>" in resp.text
    print(f"  HTML contains <h1> tag OK")
    print(f"  Content length: {len(resp.content)} bytes")


def test_custom_fallback_order() -> None:
    """Custom engine order via fallback=[...]."""
    fetch = Fetch(fallback=["curl_cffi"])
    resp = fetch.get("https://httpbin.org/get")
    print(f"\n[CUSTOM ORDER curl_cffi only] {resp}")
    assert resp.ok
    assert resp.engine == "curl_cffi"


def main() -> None:
    """Run all StealthPlex integration tests."""
    print("=" * 60)
    print("StealthPlex Integration Tests")
    print("=" * 60)

    test_stealth_get()
    test_stealth_post_json()
    test_stealth_put_data()
    test_stealth_patch()
    test_stealth_delete()
    test_stealth_head()
    test_stealth_options()
    test_stealth_headers_cookies()
    test_stealth_redirect_control()
    test_stealth_html_parse()
    test_custom_fallback_order()

    print("\n" + "=" * 60)
    print("\nAll StealthPlex tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
