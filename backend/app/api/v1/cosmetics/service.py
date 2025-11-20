from sqlalchemy.orm import Session
from .repository import list_cosmetics, get_cosmetic_by_id

def get_all_cosmetics(db: Session, params: dict):
    return list_cosmetics(db, params)

def get_details(db: Session, cosmetic_id: int):
    return get_cosmetic_by_id(db, cosmetic_id)