from app.database import SessionLocal
from app.models import Cosmetic
from app.services.fortnite import (
    fetch_cosmetics_sync,
    fetch_new_cosmetics_sync,
    fetch_shop_sync
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

def sync_cosmetics_task():
    db = SessionLocal()
    
    all_data = fetch_cosmetics_sync()
    all_items = all_data.get("data", {}).get("beans", [])

    new_data = fetch_new_cosmetics_sync()
    new_ids = {c.get("cosmeticId") for c in new_data.get("data", {}).get("beans", [])} 
    
    shop_data = fetch_cosmetics_sync()
    sale_ids = {
        item["cosmetic"]["id"]
        for section in shop_data.get("data", {}).values()
        if isinstance(section, list)
        for item in section
        if "cosmetic" in item and "id" in item["cosmetic"]
    }

    for item in all_items: 
        cosmetic_id = item.get("cosmeticId") 
        if not cosmetic_id:
            continue

        existing = db.query(Cosmetic).filter_by(id=cosmetic_id).first()
        if existing:
            existing.name = item.get("name", existing.name)
            existing.rarity = item.get("rarity", {}).get("value", existing.rarity)
            existing.price = item.get("name", existing.price)
            existing.is_new = cosmetic_id in new_ids
            existing.is_on_sale = cosmetic_id in sale_ids
        else:
            new_cosmetic = Cosmetic(
            id=cosmetic_id,
            name=item.get("name", "Desconhecido"),
            rarity=item.get("rarity", {}).get("value", "comum"),
            price=item.get("price", 0),
            is_new=cosmetic_id in new_ids,
            is_on_sale=cosmetic_id in sale_ids
        )
            db.add(new_cosmetic)

        try:
            db.commit()
        except IntegrityError:
            db.rollback

    db.close()