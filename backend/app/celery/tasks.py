from app.celery.config import celery_app
from app.database.session import SessionLocal
from app.api.v1.cosmetics.models import Cosmetic
from app.services.fortnite import (
    fetch_cosmetics_sync,
    fetch_new_cosmetics_sync,
    fetch_shop_sync
)
from sqlalchemy.exc import IntegrityError

from backend.app.api.v1.users.models import User

@celery_app.task(name="sync_cosmetics")
def sync_cosmetics():
    db = SessionLocal()
    try:
        all_data = fetch_cosmetics_sync()
        all_items = all_data.get("data", {}).get("beans", [])

        new_data = fetch_new_cosmetics_sync()
        new_ids = {c.get("cosmeticId") for c in new_data.get("data", {}).get("beans", [])} 
        
        shop_data = fetch_shop_sync()
        sale_ids = {
            item["cosmetic"]["id"]
            for section in shop_data.get("data", {}).values()
            if isinstance(section, list)
            for item in section
            if "cosmetic" in item and "id" in item["cosmetic"]
        }

        for item in all_items: 
            api_id = item.get("cosmeticId") 
            if not api_id:
                continue

            existing = db.query(Cosmetic).filter_by(api_id=api_id).first()
            if existing:
                existing.name = item.get("name", existing.name)
                existing.rarity = item.get("rarity", {}).get("value", existing.rarity)
                existing.price = item.get("price", existing.price)
                existing.is_new = api_id in new_ids
                existing.is_on_sale = api_id in sale_ids
            else:
                new_cosmetic = Cosmetic(
                    api_id=api_id,
                    name=item.get("name", "Desconhecido"),
                    rarity=item.get("rarity", {}).get("value", "comum"),
                    price=item.get("price", 0),
                    is_new=api_id in new_ids,
                    is_on_sale=api_id in sale_ids
                    )
                db.add(new_cosmetic)

    
        db.commit()
    except IntegrityError:
        db.rollback()
    finally:
        db.close()

from datetime import datetime, timedelta

@celery_app.task(name="cleanup_old_data")
def cleanup_old_data():
    db = SessionLocal()
    try:
        threshold = datetime.now() - timedelta(days=1)
        db.query(User).filter(User.created_at < threshold).delete()
        
        db.commit()
    finally:
        db.close()