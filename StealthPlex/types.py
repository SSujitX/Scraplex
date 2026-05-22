from __future__ import annotations

from typing import Literal

EngineId = Literal["wreq", "curl_cffi", "cloudscraper", "scrapling", "seleniumbase"]

DEFAULT_FALLBACK: tuple[EngineId, ...] = (
    "curl_cffi",
    "wreq",
    "cloudscraper",
    "scrapling",
    "seleniumbase",
)
