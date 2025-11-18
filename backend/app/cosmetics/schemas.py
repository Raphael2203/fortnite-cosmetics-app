from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CosmeticOut(BaseModel):
    id: int
    api_id: str
    name: str
    rarity: str
    price: int
    is_new: bool
    is_on_sale: bool

    class Config:
        from_attributes = True