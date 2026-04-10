from sqlalchemy import Boolean, Integer, String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

bundle_cosmetic = Table(
    "bundle_cosmetic",
    Base.metadata,
    Column("bundle_id", Integer, ForeignKey("bundles.id"), primary_key=True),
    Column("cosmetic_id", Integer, ForeignKey("cosmetics.id"), primary_key=True),
)

class Cosmetic(Base):
    __tablename__ = "cosmetics"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    api_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    rarity: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(Integer, default=0)
    is_new: Mapped[bool] = mapped_column(Boolean, default=False)
    is_on_sale: Mapped[bool] = mapped_column(Boolean, default=False)

    bundles: Mapped[list["Bundle"]] = relationship(
        "Bundle",
        secondary=bundle_cosmetic, 
        back_populates="cosmetics"
    )