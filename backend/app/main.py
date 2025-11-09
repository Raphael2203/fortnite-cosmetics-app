from fastapi import FastAPI
from app.routers.router import router as api_router

app = FastAPI(
    title="Loja de Cosméticos Fortnite",
    description="API para autenticação e compras de cosméticos com v-bucks.",
    version="1.0.0"
)

app.include_router(api_router)