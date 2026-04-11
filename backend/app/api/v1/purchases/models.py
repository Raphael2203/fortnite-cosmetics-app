from datetime import datetime, timezone
from sqlalchemy import Boolean, ForeignKey, Integer, String, Enum
from ..cosmetics.models import Cosmetic
from app.database.base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
import enum

class PurchaseType(enum.Enum):
    BUY = "buy"
    RETURN = "return"

class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    cosmetic_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("cosmetics.id"), nullable=True)
    bundle_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("bundles.id"), nullable=True)
    
    type: Mapped[PurchaseType] = mapped_column(Enum(PurchaseType))
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="purchases")
    cosmetic: Mapped["Cosmetic"] = relationship("Cosmetic", lazy="selectin")
    bundle = relationship("Bundle")
