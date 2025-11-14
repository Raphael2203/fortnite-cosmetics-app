from fastapi import FastAPI
from app.routers.router import router as api_router
from celery_app.tasks import sync_cosmetics_task
from celery_app import celery_app
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
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