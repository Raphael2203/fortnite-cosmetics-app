from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.purchase_service import PurchasesService
from app.api.v1.purchases.schemas import PurchaseOut
from app.api.v1.users.dependencies import get_current_user
from app.api.v1.users.models import User
from app.database.session import get_db

router = APIRouter()

@router.post("/buy/cosmetic/{cosmetic_id}", response_model=PurchaseOut)
def buy_cosmetic(cosmetic_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return PurchasesService.buy_cosmetic(db, user, cosmetic_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/return/cosmetic/{cosmetic_id}", response_model=PurchaseOut)
def return_cosmetic(cosmetic_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return PurchasesService.return_cosmetic(db, user, cosmetic_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/buy/bundle/{bundle_id}", response_model=PurchaseOut)
def buy_bundle(bundle_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return PurchasesService.buy_bundle(db, user, bundle_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/history", response_model=list[PurchaseOut])
def history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return PurchasesService.get_history(db, user)
