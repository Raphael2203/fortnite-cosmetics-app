from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers import router as api_router
from app.celery.tasks import sync_cosmetics
from app.celery.config import celery_app
from contextlib import asynccontextmanager
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # envia uma sincronização inicial ao celery se não estivermos em testes
    if os.getenv("TESTING") != "1":
        try:
            celery_app.send_task("sync_cosmetics")
            print("Sincronização inicial enviada para o celery")
        except Exception as e:
            print(f"Erro ao enviar sincronização inicial: {e}")
    yield

app = FastAPI(
    title="Loja de Cosméticos Fortnite",
    description="API para autenticação e compras de cosméticos com v-bucks.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS: permitir acessos do frontend (ajuste allow_origins em produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção coloque a URL do frontend explicitamente
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# inclui o roteador V1 que já agrega auth, users, cosmetics e purchases
app.include_router(api_router)