from sqlalchemy.orm import Session
from typing import List, Dict

from app.api.v1.auth.models import User
from app.api.v1.purchases.models import Purchase, PurchaseType
from app.api.v1.cosmetics.models import Cosmetic

class UserService:
    @staticmethod
    def list_users(db: Session, page: int = 1, per_page: int = 10) -> List[Dict]:
        offset = (page - 1) * per_page
        users = db.query(User).offset(offset).limit(per_page).all()
        result = [{"id": u.id, "email": u.email} for u in users]
        return result

    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> Dict:
        user = db.get(User, user_id)
        if not user:
            raise ValueError("User not found")

        # find cosmetics acquired by user (purchase.type == BUY)
        purchases = (
            db.query(Purchase)
            .filter(Purchase.user_id == user_id, Purchase.type == PurchaseType.BUY, Purchase.cosmetic_id != None)
            .order_by(Purchase.created_at.desc())
            .all()
        )

        cosmetics = []
        cosmetic_ids_seen = set()
        for p in purchases:
            if p.cosmetic_id and p.cosmetic_id not in cosmetic_ids_seen:
                c = db.get(Cosmetic, p.cosmetic_id)
                if c:
                    cosmetics.append({"id": c.id, "name": c.name, "price": getattr(c, "price", None), "rarity": getattr(c, "rarity", None)})
                    cosmetic_ids_seen.add(p.cosmetic_id)

        profile = {
            "id": user.id,
            "email": user.email,
            "acquired_cosmetics": cosmetics
        }
        return profile
