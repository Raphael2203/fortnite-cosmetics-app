from fastapi.testclient import TestClient
from app.api.main import app
from app.database.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database.session import get_db
from app.api.v1.cosmetics.models import Cosmetic
import pytest
from app.database.models_imports import *

SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def seed(db):
    items = [
        Cosmetic(
            api_id="a1",
            name="Galaxy Scout",
            rarity="legendary",
            price=2000,
            is_new=True,
            is_on_sale=False,
        ),
        Cosmetic(
            api_id="a2",
            name="Brite Bomber",
            rarity="rare",
            price=1200,
            is_new=False,
            is_on_sale=True,
        ),

        Cosmetic(
            api_id="a3",
            name="Renegade",
            rarity="uncommon",
            price=800,
            is_new=False,
            is_on_sale=False,
        ),
    ]
    

    db.add_all(items)
    db.commit()

@pytest.fixture(autouse=True)
def setup_and_seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    seed(db)
    db.close()

def test_list_cosmetics_with_filters():

    # filtro por raridade
    res = client.get("/cosmetics?rarity=legendary")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Galaxy Scout"
    
    # filtro is new
    res = client.get("/cosmetics?is_new=true")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["api_id"] == "a1"

    # filtro is_on_sale
    res = client.get("/cosmetics?is_on_sale=true")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["api_id"] == "a2"

    # filtro nome
    res = client.get("/cosmetics?name=ren")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["api_id"] == "a3"

def test_pagination():
    res = client.get("/cosmetics?page=1&size=2")
    assert res.status_code == 200
    data = res.json()

    assert data["total"] == 3
    assert len(data["items"]) == 2

def test_cosmetic_details():
    res = client.get(f"/cosmetics/1")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == 1
    assert "name" in data
    assert "rarity" in data
    assert "price" in data