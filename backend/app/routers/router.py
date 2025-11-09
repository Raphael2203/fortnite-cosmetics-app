from fastapi import APIRouter
from app.auth.routes import router as users

router = APIRouter()

router.include_router(users, prefix="/auth", tags=["Autenticação"])