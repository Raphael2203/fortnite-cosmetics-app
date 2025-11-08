from fastapi import FastAPI
from app.routers import cosmetics, users
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fortnite Cosmetics API", version="1.0.0")

app.include_router(cosmetics.router)
app.include_router(users.router)