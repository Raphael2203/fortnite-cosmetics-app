from fastapi import APIRouter
from .auth.routes import router as auth
from .cosmetics.routes import router as cosmetics
from .users.routes import router as users
from .purchases.routes import router as purchases

router = APIRouter()

router.include_router(auth, prefix="/auth", tags=["Autenticação"])
router.include_router(cosmetics, prefix="/cosmetics", tags=["Cosméticos"])
router.include_router(users, prefix="/users", tags=["Usuários"])
router.include_router(purchases, prefix="/purchases", tags=["Purchases"])