from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, String
from datetime import datetime
from .database import Base

bundle_cosmetic = Table(
    "bundle_cosmetic",
    Base.metadata,
    Column("bundle_id", ForeignKey("bundles.id"), primary_key=True),
    Column("cosmetic_id", ForeignKey("cosmetics.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    vbucks: Mapped[int] = mapped_column(default=10000)

class Cosmetic(Base):
    __tablename__ = "cosmetics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    rarity: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column()
    bundles: Mapped[list["Bundle"]] = relationship(
        "Bundle", secondary=bundle_cosmetic, back_populates="cosmetics"
    )

class Purchase(Base):
    __tablename__ = "purchases"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    cosmetic_id: Mapped[int] = mapped_column(ForeignKey("cosmetics.id"))
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class Return(Base):
    __tablename__ = "returns"
    id: Mapped[int] = mapped_column(primary_key=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id"))
    reason: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class Bundle(Base):
    __tablename__ = "bundles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    cosmetics: Mapped[list["Cosmetic"]] = relationship(
        "Cosmetic", secondary=bundle_cosmetic, back_populates="bundles"
    )
