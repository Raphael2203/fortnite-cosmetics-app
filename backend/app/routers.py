from fastapi import APIRouter
from app.auth.routes import router as users
from app.cosmetics.routes import router as cosmetics

router = APIRouter()

router.include_router(users, prefix="/auth", tags=["Autenticação"])
router.include_router(cosmetics, prefix="/cosmetics", tags=["Cosméticos"])