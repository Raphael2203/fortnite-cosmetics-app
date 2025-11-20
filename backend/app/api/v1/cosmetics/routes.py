from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from .schemas import CosmeticBase, CosmeticList
from .service import get_all_cosmetics, get_details

router = APIRouter(tags=["Cosmetics"])

@router.get("/", response_model=CosmeticList)
def list_cosmetics(
    page: int = 1,
    size: int = 20,
    name: str | None = None,
    rarity: str | None = None,
    is_new: bool | None = None,
    is_on_sale: bool | None = None,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * size

    params = {
        "skip": skip,
        "limit": size,
        "name": name,
        "rarity": rarity,
        "is_new": is_new,
        "is_on_sale": is_on_sale,
    }

    return get_all_cosmetics(db, params)

@router.get("/{cosmetic_id}", response_model=CosmeticBase)
def details_endpoint(cosmetic_id: int, db: Session = Depends(get_db)):
    cosmetic = get_details(db, cosmetic_id)
    if not cosmetic:
        raise HTTPException(404, "Cosmético não encontrado")
    return cosmetic