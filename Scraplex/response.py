from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from Scraplex.types import EngineId


@dataclass(frozen=True, slots=True)
class Response:
    """Scraplex Response for fallback mode only."""

    status_code: int
    headers: dict[str, str]
    content: bytes
    text: str
    url: str
    cookies: dict[str, str]
    engine: EngineId
    handle: Any
    attempts: tuple[str, ...] = field(default_factory=tuple)
