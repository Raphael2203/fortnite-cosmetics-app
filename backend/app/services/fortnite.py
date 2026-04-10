import httpx
import time
from typing import Any
from app.core.config import BASE_FORTNITE_URL, FORTNITE_HEADERS

_cache: dict = {}
CACHE_TTL = 300  # 5 minutos

def _get_cache(key: str):
    if key in _cache:
        data, timestamp = _cache[key]
        if time.time() - timestamp < CACHE_TTL:
            return data
    return None

def _set_cache(key: str, data: Any):
    _cache[key] = (data, time.time())


async def fetch_cosmetics() -> Any:
    cached = _get_cache("cosmetics")
    if cached:
        return cached

    async with httpx.AsyncClient(headers=FORTNITE_HEADERS, timeout=30) as client:
        response = await client.get(f"{BASE_FORTNITE_URL}/cosmetics")
        response.raise_for_status()
        data = response.json()
        _set_cache("cosmetics", data)
        return data


async def fetch_new_cosmetics() -> Any:
    cached = _get_cache("new_cosmetics")
    if cached:
        return cached

    async with httpx.AsyncClient(headers=FORTNITE_HEADERS, timeout=30) as client:
        response = await client.get(f"{BASE_FORTNITE_URL}/cosmetics/new")
        response.raise_for_status()
        data = response.json()
        _set_cache("new_cosmetics", data)
        return data


async def fetch_shop() -> Any:
    cached = _get_cache("shop")
    if cached:
        return cached

    async with httpx.AsyncClient(headers=FORTNITE_HEADERS, timeout=30) as client:
        response = await client.get(f"{BASE_FORTNITE_URL}/shop")
        response.raise_for_status()
        data = response.json()
        _set_cache("shop", data)
        return data