from sqlalchemy.orm import Session
from app.api.v1.auth.models import User
from app.api.v1.purchases.models import Purchase

class UsersService:

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 20):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def public_profile(db: Session, user_id: int):
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return None

        purchases = db.query(Purchase).filter(
            Purchase.user_id == user_id,
            Purchase.is_return == False
        ).all()

        return {
            "id": user.id,
            "username": user.username,
            "cosmetics": [
                {
                    "id": pr.cosmetic.id,
                    "name": pr.cosmetic.name,
                    "rarity": pr.cosmetic.rarity,
                    "type": pr.cosmetic.type
                }
                for pr in purchases
            ]
        }
