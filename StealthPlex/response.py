from __future__ import annotations

import json as _json_mod
from dataclasses import dataclass, field
from typing import Any

from StealthPlex.types import EngineId


@dataclass(frozen=True, slots=True)
class Response:
    """StealthPlex unified Response for fallback mode."""

    status_code: int
    headers: dict[str, str]
    content: bytes
    text: str
    url: str
    cookies: dict[str, str]
    engine: EngineId
    handle: Any
    attempts: tuple[str, ...] = field(default_factory=tuple)

    def json(self, **kwargs: Any) -> Any:
        """Parse response body as JSON."""
        return _json_mod.loads(self.text, **kwargs)

    @property
    def ok(self) -> bool:
        """True if status_code < 400."""
        return self.status_code < 400

    def __repr__(self) -> str:
        return (
            f"<Response [{self.status_code}] "
            f"engine={self.engine!r} "
            f"attempts={len(self.attempts)}>"
        )
