from __future__ import annotations


class StealthPlexError(Exception):
    """Base StealthPlex error."""


class EngineUnavailable(StealthPlexError):
    """Engine extra not installed."""

    def __init__(self, engine: str, reason: str) -> None:
        self.engine = engine
        self.reason = reason
        super().__init__(f"engine {engine!r} unavailable: {reason}")


class EngineNotImplemented(StealthPlexError):
    """Engine id has no adapter yet."""

    def __init__(self, engine: str) -> None:
        self.engine = engine
        super().__init__(f"engine {engine!r} is not implemented yet")


class FetchConfigError(StealthPlexError):
    """Invalid Fetch(engine=) and Fetch(fallback=) combination."""


class ClientConfigError(FetchConfigError):
    """Deprecated alias for FetchConfigError."""


class EscalationExhausted(StealthPlexError):
    """Fallback chain exhausted."""

    def __init__(self, url: str, engines_tried: list[str]) -> None:
        self.url = url
        self.engines_tried = engines_tried
        super().__init__(f"all engines failed for {url!r}: tried {engines_tried!r}")


class FetchError(StealthPlexError):
    """Engine request failed before response."""
