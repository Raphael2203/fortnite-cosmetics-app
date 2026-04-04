import pytest
from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.api.main import app
from app.database.base import Base
from app.database.session import get_db
from app.api.v1.users.dependencies import get_current_user
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

def setup_test_data():
    db = next(override_get_db())

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    user = User(email="test@exemplo.com", hashed_password="123456", vbucks=10000)
    db.add(user)
    db.flush()

    cosmetic1 = Cosmetic(name="Skin A", price=500, api_id=1, rarity="raro")
    cosmetic2 = Cosmetic(name="Skin B", price=300, api_id=2, rarity="comum")
    db.add_all([cosmetic1, cosmetic2])
    db.flush()

    bundle1 = Bundle(name="Bundle A")
    db.add(bundle1)
    db.flush()

    db.commit()

    # store the test user id so we can always fetch the user from the request DB session
    app.state.test_user_id = user.id

    # override that retrieves the User from the current request session (override_get_db)
    def override_get_current_user(db = Depends(override_get_db)):
        return db.get(User, app.state.test_user_id)

    app.dependency_overrides[get_current_user] = override_get_current_user

    return {
        "user_id": user.id,
        "cosmetic_ids": [cosmetic1.id, cosmetic2.id],
        "bundle_id": bundle1.id  # changed: return integer instead of list
    }

@pytest.fixture
def test_data():
    return setup_test_data()

def test_buy_cosmetic(test_data):
    cosmetic_id = test_data["cosmetic_ids"][0]
    response = client.post(f"/purchases/buy/cosmetic/{cosmetic_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["cosmetic_id"] == cosmetic_id
    assert data["user_id"] == test_data["user_id"]


def test_buy_bundle(test_data):
    bundle_id = test_data["bundle_id"]
    response = client.post(f"/purchases/buy/bundle/{bundle_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["bundle_id"] == bundle_id
    assert data["user_id"] == test_data["user_id"]


def test_return_cosmetic(test_data):
    cosmetic_id = test_data["cosmetic_ids"][1]
    # compra primeiro
    buy_resp = client.post(f"/purchases/buy/cosmetic/{cosmetic_id}")
    purchase_id = buy_resp.json()["id"]

    # retorna
    response = client.post(f"/purchases/return/cosmetic/{cosmetic_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["cosmetic_id"] == cosmetic_id


def test_history(test_data):
    response = client.get("/purchases/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)