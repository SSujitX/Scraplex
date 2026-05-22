from __future__ import annotations

from StealthPlex.response import Response
from StealthPlex.types import DEFAULT_FALLBACK, EngineId

_BLOCKED = frozenset({403, 429, 503})


def should_escalate(response: Response) -> bool:
    """True if response looks blocked."""
    if response.status_code in _BLOCKED:
        return True
    body = response.text.lower()
    return any(m in body for m in ("cloudflare", "cf-browser-verification", "challenge"))


def resolve_fallback_chain(
    *,
    use_default: bool,
    explicit: list[EngineId] | None,
    installed: tuple[EngineId, ...],
) -> tuple[EngineId, ...]:
    """Ordered engine ids for fallback."""
    if explicit is not None:
        source = tuple(explicit)
    elif use_default:
        source = DEFAULT_FALLBACK
    else:
        return ()
    ok = set(installed)
    return tuple(e for e in source if e in ok)
