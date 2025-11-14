from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, String, Boolean, Integer
from datetime import datetime
from .database import Base

bundle_cosmetic = Table(
    "bundle_cosmetic",
    Base.metadata,
    Column("bundle_id", Integer, ForeignKey("bundles.id"), primary_key=True),
    Column("cosmetic_id", Integer, ForeignKey("cosmetics.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    vbucks: Mapped[int] = mapped_column(Integer, default=10000)
    purchases: Mapped[list["Purchase"]] = relationship(back_populates="user")

class Cosmetic(Base):
    __tablename__ = "cosmetics"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    api_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    rarity: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(Integer)
    is_new: Mapped[bool] = mapped_column(Boolean, default=False)
    is_on_sale: Mapped[bool] = mapped_column(Boolean, default=False)
    bundles: Mapped[list["Bundle"]] = relationship(
        "Bundle", secondary=bundle_cosmetic, back_populates="cosmetics"
    )

class Purchase(Base):
    __tablename__ = "purchases"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    cosmetic_id: Mapped[int] = mapped_column(Integer, ForeignKey("cosmetics.id"), onupdate="CASCADE")
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="purchases")
    cosmetic: Mapped["Cosmetic"] = relationship()

class Return(Base):
    __tablename__ = "returns"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    purchase_id: Mapped[int] = mapped_column(Integer, ForeignKey("purchases.id"))
    reason: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    purchase: Mapped["Purchase"] = relationship()

class Bundle(Base):
    __tablename__ = "bundles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    cosmetics: Mapped[list["Cosmetic"]] = relationship(
        "Cosmetic", secondary=bundle_cosmetic, back_populates="bundles"
    )
