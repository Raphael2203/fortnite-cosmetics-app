import httpx
from typing import Any

BASE_URL = "https://fortnite-api.com/v2"
HEADERS = {"User-Agent": "FortniteApp/1.0"}

async def fetch_cosmetics() -> Any:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/cosmetics")
        response.raise_for_status()
        return response.json()
    
async def fetch_new_cosmetics() -> Any:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/cosmetics/new")
        response.raise_for_status()
        return response.json()
    
async def fetch_shop() -> Any:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/shop")
        response.raise_for_status()
        return response.json()
    
def fetch_cosmetics_sync() -> dict:
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/cosmetics", headers=HEADERS)
        response.raise_for_status()
        return response.json()
    
def fetch_new_cosmetics_sync() -> dict:
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/cosmetics/new", headers=HEADERS)
        response.raise_for_status()
        return response.json()
    
def fetch_shop_sync() -> dict:
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/shop", headers=HEADERS)
        response.raise_for_status()
        return response.json()