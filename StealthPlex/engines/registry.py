from __future__ import annotations

from collections.abc import Callable

from StealthPlex.engines.base import Engine
from StealthPlex.engines.cloudscraper import CloudscraperEngine
from StealthPlex.engines.curl_cffi import CurlCffiEngine
from StealthPlex.engines.scrapling import ScraplingEngine
from StealthPlex.engines.seleniumbase import SeleniumBaseEngine
from StealthPlex.engines.wreq import WreqEngine
from StealthPlex.exceptions import EngineNotImplemented, EngineUnavailable
from StealthPlex.types import EngineId

EngineFactory = Callable[[], Engine]

_REGISTRY: dict[EngineId, EngineFactory] = {
    "wreq": WreqEngine,
    "curl_cffi": CurlCffiEngine,
    "cloudscraper": CloudscraperEngine,
    "scrapling": ScraplingEngine,
    "seleniumbase": SeleniumBaseEngine,
}


def register_engine(engine_id: EngineId, factory: EngineFactory) -> None:
    """Register engine factory; engine_id key, factory returns Engine instance."""
    _REGISTRY[engine_id] = factory


def create_engine(engine_id: EngineId) -> Engine:
    """Instantiate engine by id; raises EngineNotImplemented or EngineUnavailable."""
    factory = _REGISTRY.get(engine_id)
    if factory is None:
        raise EngineNotImplemented(engine_id)
    engine = factory()
    if not engine.installed():
        raise EngineUnavailable(engine_id, f"install StealthPlex[{engine_id}]")
    return engine


def installed_engine_ids() -> tuple[EngineId, ...]:
    """Return registered engine ids with installed optional dependencies."""
    available: list[EngineId] = []
    for engine_id, factory in _REGISTRY.items():
        if factory().installed():
            available.append(engine_id)
    return tuple(available)
