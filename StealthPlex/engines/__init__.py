from __future__ import annotations

from StealthPlex.engines.base import Engine
from StealthPlex.engines.curl_cffi import CurlCffiEngine, CurlCffiProxy
from StealthPlex.engines.registry import create_engine, installed_engine_ids, register_engine
from StealthPlex.engines.scrapling import ScraplingEngine, ScraplingProxy
from StealthPlex.engines.wreq import WreqEngine, WreqProxy

__all__ = [
    "CurlCffiEngine",
    "CurlCffiProxy",
    "Engine",
    "ScraplingEngine",
    "ScraplingProxy",
    "WreqEngine",
    "WreqProxy",
    "create_engine",
    "installed_engine_ids",
    "register_engine",
]
