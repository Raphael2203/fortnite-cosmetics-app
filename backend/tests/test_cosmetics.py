from fastapi.testclient import TestClient
from app.main import app
from app.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.models import Cosmetic

SQLALCHEMY_DATABASE_URL = "sqlite:///./.test_cosmetics.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

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

def test_list_cosmetics_with_filters():
    db = TestingSessionLocal()
    seed(db)

    res = client.get("/cosmetics?rarity=legendary")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 1
    assert data["items"][0][]