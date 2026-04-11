from typing import Optional

from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class CosmeticBase(BaseModel):
    id: int
    api_id: str
    name: str
    rarity: str
    price: int
    is_new: bool
    is_on_sale: bool
    image_url: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class CosmeticList(BaseModel):
    total: int
    items: list[CosmeticBase]