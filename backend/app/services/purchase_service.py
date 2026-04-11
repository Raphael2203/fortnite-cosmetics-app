from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.api.v1.purchases.models import Purchase, PurchaseType
from app.api.v1.cosmetics.models import Cosmetic
from app.api.v1.bundles.models import Bundle

class PurchasesService:
    @staticmethod
    def buy_cosmetic(db: Session, user, cosmetic_id: int) -> Purchase:
        cosmetic = db.query(Cosmetic).filter_by(id=cosmetic_id).first()
        if not cosmetic:
            raise ValueError("Cosmetic not found")
        
        existing = db.query(Purchase).filter(
            Purchase.user_id == user.id,
            Purchase.cosmetic_id == cosmetic_id,
            Purchase.type == PurchaseType.BUY
        ).first()
        if existing:
            raise ValueError("Você já possui este item")

        price = getattr(cosmetic, "price", 0) or 0
        if getattr(user, "vbucks", 0) < price:
            raise ValueError("Insufficient v-bucks")

        user.vbucks = user.vbucks - price
        purchase = Purchase(
            user_id=user.id,
            cosmetic_id=cosmetic.id,
            bundle_id=None,
            type=PurchaseType.BUY
        )
        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        return purchase

    @staticmethod
    def return_cosmetic(db: Session, user, cosmetic_id: int) -> Purchase:
        original_purchase = db.query(Purchase).filter(
            Purchase.user_id == user.id,
            Purchase.cosmetic_id == cosmetic_id,
            Purchase.type == PurchaseType.BUY
        ).first()

        if not original_purchase:
            raise ValueError("Você não possui este item para devolver")

        cosmetic = db.query(Cosmetic).filter_by(id=cosmetic_id).first()
        price = getattr(cosmetic, "price", 0) or 0
        user.vbucks = user.vbucks + price

        db.delete(original_purchase)
        return_entry = Purchase(
            user_id=user.id,
            cosmetic_id=cosmetic_id,
            bundle_id=None,
            type=PurchaseType.RETURN
        )
        
        db.add(return_entry)
        db.commit()
        db.refresh(return_entry)
        return return_entry

    @staticmethod
    def get_history(db: Session, user):
        from sqlalchemy.orm import joinedload
        return db.query(Purchase).options(joinedload(Purchase.cosmetic))\
            .filter_by(user_id=user.id)\
            .order_by(Purchase.created_at.desc()).all()