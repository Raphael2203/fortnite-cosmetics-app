from sqlalchemy.orm import Session
from typing import List, Dict

# Ajuste os caminhos de acordo com sua nova estrutura
from app.api.v1.users.models import User 
from app.api.v1.purchases.models import Purchase, PurchaseType
from app.api.v1.cosmetics.models import Cosmetic

class UserService:
    @staticmethod
    def list_users(db: Session, page: int = 1, per_page: int = 10) -> List[Dict]:
        offset = (page - 1) * per_page
        users = db.query(User).offset(offset).limit(per_page).all()
        return [{"id": u.id, "email": u.email} for u in users]

    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> Dict:
        # Busca o usuário
        user = db.get(User, user_id)
        if not user:
            raise ValueError("Usuário não encontrado")

        # Busca as compras de cosméticos do usuário (Tipo BUY)
        # Usamos join para buscar os dados do cosmético de uma vez só (mais rápido)
        purchases = (
            db.query(Purchase)
            .join(Cosmetic, Purchase.cosmetic_id == Cosmetic.id)
            .filter(
                Purchase.user_id == user_id, 
                Purchase.type == PurchaseType.BUY,
                Purchase.cosmetic_id.isnot(None)
            )
            .order_by(Purchase.created_at.desc())
            .all()
        )

        cosmetics = []
        cosmetic_ids_seen = set()
        
        for p in purchases:
            # Como fizemos o join, o objeto Cosmetic já está "atachado" à compra
            c = p.cosmetic 
            if c and c.id not in cosmetic_ids_seen:
                cosmetics.append({
                    "id": c.id, 
                    "name": c.name, 
                    "price": getattr(c, "price", 0), 
                    "rarity": getattr(c, "rarity", "comum")
                })
                cosmetic_ids_seen.add(c.id)

        return {
            "id": user.id,
            "email": user.email,
            "vbucks": getattr(user, "vbucks", 0), # Adicionei vbucks para o seu front
            "acquired_cosmetics": cosmetics
        }