from sqlalchemy.orm import Session
from ..cosmetics.models import Cosmetic

def list_cosmetics(db: Session, params: dict):
    query = db.query(Cosmetic)

    if params.get("name"):
        query = query.filter(Cosmetic.name.ilike(f"%{params['name']}%"))
    
    if params.get("rarity"):
        query = query.filter(Cosmetic.rarity == params["rarity"])
    
    if params.get("is_new") is not None:
        query = query.filter(Cosmetic.is_new == params["is_new"])
    
    if params.get("is_on_sale") is not None:
        query = query.filter(Cosmetic.is_on_sale == params["is_on_sale"])

    total = query.count()

    items = query.offset(params["skip"]).limit(params["limit"]).all()

    return {"total": total, "items": items}

def get_cosmetic_by_id(db: Session, cosmetic_id: int):
    return db.query(Cosmetic).filter(Cosmetic.id == cosmetic_id).first()