from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PurchaseCreate(BaseModel):
    cosmetic_id: Optional[int] = None
    bundle_id: Optional[int] = None
    type: str
    
class PurchaseOut(BaseModel):
    id: int
    user_id: int
    cosmetic_id: Optional[int]
    bundle_id: Optional[int]
    type: str

    class Config:
        orm_mode = True