from fastapi import FastAPI
from app.api.v1.routers import router as api_router
from app.api.v1.users.routes import router as users_router
from app.celery.tasks import sync_cosmetics
from app.celery.config import celery_app
from contextlib import asynccontextmanager
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("TESTING") != "1":
        try:
            celery_app.send_task("sync_cosmetics")
            print("Sincronização inicial enviada para o celery")
        except Exception as e:
            print(f"Erro ao enviar sncronização inicial: {e}")
        yield
    
app = FastAPI(
    title="Loja de Cosméticos Fortnite",
    description="API para autenticação e compras de cosméticos com v-bucks.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)
app.include_router(users_router, prefix="/users", tags=["users"])