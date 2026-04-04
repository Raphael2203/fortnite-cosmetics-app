from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers import router as api_router

app = FastAPI(
    title="Loja de Cosméticos Fortnite",
    description="API para autenticação e compras de cosméticos com v-bucks.",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",                         
    "https://fortnite-cosmetics-front.vercel.app",      
    "https://fortnite-cosmetics-front-fy0777yl3-raphael2203s-projects.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)