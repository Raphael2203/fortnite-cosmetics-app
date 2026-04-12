from fastapi import APIRouter, Response, status
from sqlalchemy import text

from app.database.session import SessionLocal
from .cosmetics.routes import router as cosmetics
from .users.routes import router as users
from .purchases.routes import router as purchases

router = APIRouter()

@router.get("/health")
def health_check(response: Response):
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1")).fetchone()
        return {"status": "online"}
    except Exception as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return{"status": "starting", "details": str(e)}
    finally:
        db.close()

router.include_router(cosmetics, prefix="/cosmetics", tags=["Cosméticos"])
router.include_router(users, prefix="/users", tags=["Usuários"])
router.include_router(purchases, prefix="/purchases", tags=["Purchases"])