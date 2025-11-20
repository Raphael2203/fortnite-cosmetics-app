from fastapi.testclient import TestClient
from app.api.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database.session import get_db
from app.database.base import Base
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

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_register_login_me():
    res = client.post("/auth/register", json={
        "email": "test@exemplo.com",
        "password": "123456"
    })

    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "test@exemplo.com"
    assert "id" in data

    res = client.post("/auth/login", json={
        "email": "test@exemplo.com",
        "password": "123456"
    })

    assert res.status_code == 200
    token = res.json()["access_token"]
    assert token is not None

    res = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 200
    me = res.json()
    assert me["email"] == "test@exemplo.com"