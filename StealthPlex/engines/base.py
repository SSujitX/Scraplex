from __future__ import annotations

from typing import Any, Protocol

from StealthPlex.response import Response
from StealthPlex.types import EngineId


class Engine(Protocol):
    """Engine adapter for fallback chain; id name, installed check, request method."""

    @property
    def id(self) -> EngineId:
        """Engine identifier string."""
        ...

    def installed(self) -> bool:
        """True when optional dependency is importable."""
        ...

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        timeout: float | None = None,
    ) -> Response:
        """Perform HTTP request; returns StealthPlex Response."""
        ...
