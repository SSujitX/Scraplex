from __future__ import annotations

from types import ModuleType
from typing import Any

from StealthPlex.engines.seleniumbase._docs import PROXY_CLASS
from StealthPlex.types import EngineId

_PUBLIC = (
    "SB",
    "Driver",
    "DriverContext",
    "BaseCase",
    "get_driver",
    "MasterQA",
    "sb_cdp",
    "cdp_driver",
    "decorators",
    "common",
    "config",
    "core",
    "extensions",
    "fixtures",
    "drivers",
    "plugins",
    "masterqa",
    "page_actions",
    "page_utils",
    "js_utils",
    "translate",
    "undetected",
    "version_info",
    "version_list",
    "version_tuple",
)


def _pkg() -> ModuleType:
    import seleniumbase

    return seleniumbase


class SeleniumBaseProxy:
    """seleniumbase module proxy; hover ``fetch`` after ``Fetch(engine=\"seleniumbase\")``."""

    __doc__ = PROXY_CLASS

    def __init__(self) -> None:
        """Bind seleniumbase API; requires StealthPlex[seleniumbase]."""
        mod = _pkg()
        object.__setattr__(self, "_module", mod)
        for name in _PUBLIC:
            if hasattr(mod, name):
                object.__setattr__(self, name, getattr(mod, name))
        version = getattr(mod, "__version__", None)
        if version is not None:
            object.__setattr__(self, "__version__", version)

    def __getattr__(self, name: str) -> Any:
        return getattr(object.__getattribute__(self, "_module"), name)

    @property
    def id(self) -> EngineId:
        return "seleniumbase"

    def installed(self) -> bool:
        try:
            _pkg()
            return True
        except ImportError:
            return False
