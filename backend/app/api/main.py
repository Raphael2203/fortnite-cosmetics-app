import threading
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers import router as api_router
from app.database.session import SessionLocal
from app.database.seed import seed_test_user
from app.services.sync_service import run_initial_sync

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_test_user(db)
    finally:
        db.close()
    
    sync_thread = threading.Thread(target=run_initial_sync)
    sync_thread.start()

    yield
    
app = FastAPI(
    lifespan=lifespan,
    title="Loja de Cosméticos Fortnite",
    description="API para autenticação e compras de cosméticos com v-bucks.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "ok"}

origins = [
    "http://localhost:4173",
    "http://127.0.0.1:4173",                         
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