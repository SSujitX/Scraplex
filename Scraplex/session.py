from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Session:
    """Internal cookie/header state for fallback client — not curl_cffi.Session."""

    cookies: dict[str, str] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)

    def merge_headers(self, headers: dict[str, str] | None) -> dict[str, str]:
        """Merge session and request headers."""
        if not headers:
            return dict(self.headers)
        merged = dict(self.headers)
        merged.update(headers)
        return merged
