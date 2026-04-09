from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers import router as api_router
from app.database.session import SessionLocal
from app.database.seed import seed_test_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_test_user(db)
    finally:
        db.close()
    yield
    
app = FastAPI(
    lifespan=lifespan,
    title="Loja de Cosméticos Fortnite",
    description="API para autenticação e compras de cosméticos com v-bucks.",
    version="1.0.0"
)

origins = [
    "http://localhost:4173",
    "http://127.0.0.1:4173"                         
    "https://fortnite-cosmetics-front.vercel.app",      
    "https://fortnite-cosmetics-front-g28lsnodz-raphael2203s-projects.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")