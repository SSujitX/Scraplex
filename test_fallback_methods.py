"""Integration test for testing all FallbackClient HTTP methods and parameters.

Run:
    uv run test_fallback_methods.py
"""

from __future__ import annotations

import json
from StealthPlex import Fetch


def test_fallback_http_methods() -> None:
    # Use fallback with curl_cffi and wreq for testing HTTP methods synchronously
    fetch = Fetch(fallback=True)

    print("--- 1. Testing GET ---")
    resp_get = fetch.get(
        "https://httpbin.org/get",
        headers={"X-Test-Header": "HelloGet"},
        params={"foo": "bar"},
        cookies={"my_cookie": "cookie_value"},
    )
    print(f"GET Status: {resp_get.status_code}, Engine: {resp_get.engine}")
    assert resp_get.status_code == 200
    try:
        data = json.loads(resp_get.text)
        print("GET headers received by server:", data.get("headers"))
        print("GET args received by server:", data.get("args"))
        assert data["headers"].get("X-Test-Header") == "HelloGet"
        assert data["args"].get("foo") == "bar"
        cookie_header = data["headers"].get("Cookie", "")
        print("GET Cookie header received by server:", cookie_header)
        assert "my_cookie=cookie_value" in cookie_header
    except Exception as e:
        print(f"Error parsing GET response: {e}")
        raise e

    print("\n--- 2. Testing POST with JSON ---")
    resp_post = fetch.post(
        "https://httpbin.org/post",
        headers={"X-Test-Header": "HelloPost"},
        json={"post_key": "post_val"},
    )
    print(f"POST Status: {resp_post.status_code}, Engine: {resp_post.engine}")
    assert resp_post.status_code == 200
    try:
        data = json.loads(resp_post.text)
        print("POST JSON received by server:", data.get("json"))
        assert data["json"].get("post_key") == "post_val"
    except Exception as e:
        print(f"Error parsing POST response: {e}")
        raise e

    print("\n--- 3. Testing PUT with data ---")
    resp_put = fetch.put(
        "https://httpbin.org/put",
        data="hello put",
    )
    print(f"PUT Status: {resp_put.status_code}, Engine: {resp_put.engine}")
    assert resp_put.status_code == 200
    try:
        data = json.loads(resp_put.text)
        print("PUT data received by server:", data.get("data"))
        assert data["data"] == "hello put"
    except Exception as e:
        print(f"Error parsing PUT response: {e}")
        raise e

    print("\n--- 4. Testing DELETE ---")
    resp_delete = fetch.delete("https://httpbin.org/delete")
    print(f"DELETE Status: {resp_delete.status_code}, Engine: {resp_delete.engine}")
    assert resp_delete.status_code == 200

    print("\n--- 5. Testing HEAD ---")
    # For HEAD, most servers don't return a body, and curl_cffi supports HEAD
    resp_head = fetch.head("https://httpbin.org/get")
    print(f"HEAD Status: {resp_head.status_code}, Engine: {resp_head.engine}")
    assert resp_head.status_code == 200

    print("\n--- 6. Testing OPTIONS ---")
    resp_options = fetch.options("https://httpbin.org/get")
    print(f"OPTIONS Status: {resp_options.status_code}, Engine: {resp_options.engine}")
    assert resp_options.status_code == 200

    print("\n--- 7. Testing PATCH ---")
    resp_patch = fetch.patch("https://httpbin.org/patch", json={"patch_key": "patch_val"})
    print(f"PATCH Status: {resp_patch.status_code}, Engine: {resp_patch.engine}")
    assert resp_patch.status_code == 200
    try:
        data = json.loads(resp_patch.text)
        print("PATCH JSON received by server:", data.get("json"))
        assert data["json"].get("patch_key") == "patch_val"
    except Exception as e:
        print(f"Error parsing PATCH response: {e}")
        raise e

    print("\n--- 8. Testing Redirect Behavior ---")
    # Test allow_redirects=False (expect redirect status code e.g. 302)
    resp_redirect = fetch.get("https://httpbin.org/redirect/1", allow_redirects=False)
    print(f"Redirect Status (allow_redirects=False): {resp_redirect.status_code}, Engine: {resp_redirect.engine}")
    assert 300 <= resp_redirect.status_code < 400

    # Test redirect=False (legacy/alternate kwarg)
    resp_redirect_alt = fetch.get("https://httpbin.org/redirect/1", redirect=False)
    print(f"Redirect Status (redirect=False): {resp_redirect_alt.status_code}, Engine: {resp_redirect_alt.engine}")
    assert 300 <= resp_redirect_alt.status_code < 400


if __name__ == "__main__":
    test_fallback_http_methods()
    print("\nAll Fallback HTTP methods integration tests passed!")
