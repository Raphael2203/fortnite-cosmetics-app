from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Integer, String
from ..cosmetics.models import Cosmetic
from app.database.base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column

class Purchase(Base):
    __tablename__ = "purchases"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    cosmetic_id: Mapped[int] = mapped_column(Integer, ForeignKey("cosmetics.id"), onupdate="CASCADE")
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="purchases")
    cosmetic: Mapped["Cosmetic"] = relationship()

class Return(Base):
    __tablename__ = "returns"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    purchase_id: Mapped[int] = mapped_column(Integer, ForeignKey("purchases.id"))
    reason: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    purchase: Mapped["Purchase"] = relationship()

from ..auth.models import User
