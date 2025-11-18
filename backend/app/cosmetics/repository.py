from sqlalchemy.orm import Session
from app.models import Cosmetic

def list_cosmetics(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        name: str | None = None,
        rarity: str | None = None,
        is_new: bool | None = None,
        is_on_sale: bool | None = None,
):
    query = db.query(Cosmetic)

    if name:
        query = query.filter(Cosmetic.name.ilike(f"%{name}%"))
    elif rarity:
        query = query.filter(Cosmetic.rarity == rarity)
    elif is_new is not None:
        query = query.filter(Cosmetic.is_new == is_new)
    elif is_on_sale is not None:
        query = query.filter(Cosmetic.is_on_sale == is_on_sale)

    return query.offset(skip).limit(limit).all()

def get_cosmetic_by_id(db: Session, cosmetic_id: int):
    return db.query(Cosmetic).filter(Cosmetic.id == cosmetic_id).first()