from typing import Dict, Any
import time

CACHE_TTL = 60 

_cache: Dict[str, Dict[str, Any]] = {}


def get_cache(key: str):
    entry = _cache.get(key)
    if not entry:
        return None

    if time.time() - entry["time"] > CACHE_TTL:
        del _cache[key]
        return None

    return entry["value"]


def set_cache(key: str, value: Any):
    _cache[key] = {
        "value": value,
        "time": time.time()
    }


def clear_cache(key: str = None):
    if key:
        _cache.pop(key, None)
    else:
        _cache.clear()
