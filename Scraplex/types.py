from __future__ import annotations

from typing import Literal

EngineId = Literal["wreq", "curl_cffi", "cloudscraper", "scrapling", "seleniumbase"]

DEFAULT_FALLBACK: tuple[EngineId, ...] = (
    "wreq",
    "curl_cffi",
    "cloudscraper",
    "scrapling",
    "seleniumbase",
)
