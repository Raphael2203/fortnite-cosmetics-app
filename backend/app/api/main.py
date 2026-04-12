import threading
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from app.api.v1.routers import router as api_router
from app.database.session import SessionLocal
from app.database.seed import maintenance_and_seed_db
from app.services.sync_service import run_initial_sync
from sqlalchemy import text

def run_db_maintenance():
    """Função auxiliar para ser chamada pelo agendador"""
    db = SessionLocal()
    try:
        maintenance_and_seed_db(db)
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    run_db_maintenance()
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_db_maintenance, 'cron', hour=0, minute=0)
    scheduler.add_job(lambda: SessionLocal().execute(text("SELECT 1")), 'interval', minutes=15)
    scheduler.start()
    sync_thread = threading.Thread(target=run_initial_sync)
    sync_thread.start()

    yield
    scheduler.shutdown()

app = FastAPI(
    lifespan=lifespan,
    title="Loja de Cosméticos Fortnite",
    description="API para autenticação e compras de cosméticos com v-bucks.",
    version="1.0.0"
)

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