from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import ForeignKey
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    vbucks: Mapped[int] = mapped_column(default=10000)

class Cosmetic(Base):
    __tablename__ = "cosmetics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    rarity: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()

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
    reason: Mapped[str] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class Bundle(Base):
    __tablename__ = "bundles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    cosmetics_ids: Mapped[list[int]] = mapped_column()