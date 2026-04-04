from fastapi import APIRouter, HTTPException
from .users.routes import router as auth
from .cosmetics.routes import router as cosmetics
from .users.routes import router as users
from .purchases.routes import router as purchases
from app.celery.config import celery_app

router = APIRouter()

@router.post("/admin/sync", tags=["Admin"])
async def trigger_sync():
    try:
        celery_app.send_task("sync_cosmetics")
        return {"status": "success", "message": "Sincronização enviada para a fila do Celery."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao disparar tarefa: {str(e)}")

router.include_router(cosmetics, prefix="/cosmetics", tags=["Cosméticos"])
router.include_router(users, prefix="/users", tags=["Usuários"])
router.include_router(purchases, prefix="/purchases", tags=["Purchases"])