from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from sqlalchemy import String, Integer

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    vbucks: Mapped[int] = mapped_column(Integer, default=10000)

    purchases: Mapped[list["Purchase"]] = relationship(
        back_populates="user", 
        lazy="selectin"
        )


from ..purchases.models import Purchase