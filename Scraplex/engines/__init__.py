from __future__ import annotations

from Scraplex.engines.base import Engine
from Scraplex.engines.curl_cffi import CurlCffiEngine, CurlCffiProxy
from Scraplex.engines.registry import create_engine, installed_engine_ids, register_engine
from Scraplex.engines.scrapling import ScraplingEngine, ScraplingProxy
from Scraplex.engines.wreq import WreqEngine, WreqProxy

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
