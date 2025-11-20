import httpx
from typing import Any
from app.core.config import BASE_FORTNITE_URL, FORTNITE_HEADERS


async def fetch_cosmetics() -> Any:
    async with httpx.AsyncClient(headers=FORTNITE_HEADERS) as client:
        response = await client.get(f"{BASE_FORTNITE_URL}/cosmetics")
        response.raise_for_status()
        return response.json()


async def fetch_new_cosmetics() -> Any:
    async with httpx.AsyncClient(headers=FORTNITE_HEADERS) as client:
        response = await client.get(f"{BASE_FORTNITE_URL}/cosmetics/new")
        response.raise_for_status()
        return response.json()


async def fetch_shop() -> Any:
    async with httpx.AsyncClient(headers=FORTNITE_HEADERS) as client:
        response = await client.get(f"{BASE_FORTNITE_URL}/shop")
        response.raise_for_status()
        return response.json()


def fetch_cosmetics_sync() -> dict:
    with httpx.Client(headers=FORTNITE_HEADERS) as client:
        response = client.get(f"{BASE_FORTNITE_URL}/cosmetics")
        response.raise_for_status()
        return response.json()


def fetch_new_cosmetics_sync() -> dict:
    with httpx.Client(headers=FORTNITE_HEADERS) as client:
        response = client.get(f"{BASE_FORTNITE_URL}/cosmetics/new")
        response.raise_for_status()
        return response.json()


def fetch_shop_sync() -> dict:
    with httpx.Client(headers=FORTNITE_HEADERS) as client:
        response = client.get(f"{BASE_FORTNITE_URL}/shop")
        response.raise_for_status()
        return response.json()
