from datetime import datetime, timezone
from sqlalchemy.orm import Session

# make sure these imports match your project structure
from app.api.v1.purchases.models import Purchase, PurchaseType
from app.api.v1.cosmetics.models import Cosmetic
from app.api.v1.bundles.models import Bundle

class PurchasesService:
    @staticmethod
    def buy_cosmetic(db: Session, user, cosmetic_id: int) -> Purchase:
        # fetch cosmetic
        cosmetic = db.query(Cosmetic).filter_by(id=cosmetic_id).first()
        if not cosmetic:
            raise ValueError("Cosmetic not found")

        # check vbucks if price available
        price = getattr(cosmetic, "price", 0) or 0
        if getattr(user, "vbucks", 0) < price:
            raise ValueError("Insufficient v-bucks")

        # deduct and create purchase
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
    def buy_bundle(db: Session, user, bundle_id: int) -> Purchase:
        bundle = db.query(Bundle).filter_by(id=bundle_id).first()
        if not bundle:
            raise ValueError("Bundle not found")

        # minimal behaviour: register a bundle purchase. If you want to deduct sum of cosmetics,
        # compute sum via related cosmetics and deduct from user.vbucks here.
        purchase = Purchase(
            user_id=user.id,
            cosmetic_id=None,
            bundle_id=bundle.id,
            type=PurchaseType.BUY
        )
        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        return purchase

    @staticmethod
    def return_cosmetic(db: Session, user, cosmetic_id: int) -> Purchase:
        # minimal behaviour: create a RETURN purchase entry and (optionally) refund v-bucks
        cosmetic = db.query(Cosmetic).filter_by(id=cosmetic_id).first()
        if not cosmetic:
            raise ValueError("Cosmetic not found")

        # optional: find last buy purchase for this cosmetic to compute refund
        # here we refund the cosmetic.price if exists
        price = getattr(cosmetic, "price", 0) or 0
        user.vbucks = user.vbucks + price

        purchase = Purchase(
            user_id=user.id,
            cosmetic_id=cosmetic.id,
            bundle_id=None,
            type=PurchaseType.RETURN
        )
        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        return purchase

    @staticmethod
    def get_history(db: Session, user):
        return db.query(Purchase).filter_by(user_id=user.id).order_by(Purchase.created_at.desc()).all()
