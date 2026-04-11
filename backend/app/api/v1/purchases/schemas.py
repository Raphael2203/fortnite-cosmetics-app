from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CosmeticMinOut(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None
    rarity: str
    price: int

    class Config:
        from_attributes = True

class PurchaseOut(BaseModel):
    id: int
    user_id: int
    type: str
    created_at: datetime
    cosmetic: Optional[CosmeticMinOut] = None 
    bundle_id: Optional[int] = None

    class Config:
        from_attributes = True