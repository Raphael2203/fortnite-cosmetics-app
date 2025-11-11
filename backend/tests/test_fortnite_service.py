import pytest
import asyncio
from app.services import fortnite

@pytest.mark.asyncio
async def test_fetch_cosmetics():
    data = await fortnite.fetch_cosmetics()
    assert "data" in data
    assert "beans" in data["data"]
    assert isinstance(data["data"]["beans"], list)

@pytest.mark.asyncio
async def test_fetch_new_cosmetics():
    data = await fortnite.fetch_new_cosmetics()
    assert "data" in data

@pytest.mark.asyncio
async def test_fetch_shop():
    data = await fortnite.fetch_shop()
    assert "data" in data