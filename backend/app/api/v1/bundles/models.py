from __future__ import annotations

from sqlalchemy import Integer, String
from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..cosmetics.models import bundle_cosmetic

class Bundle(Base):
    __tablename__ = "bundles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    cosmetics: Mapped[list["Cosmetic"]] = relationship(
        "Cosmetic", 
        secondary=bundle_cosmetic, 
        back_populates="bundles",
    )

