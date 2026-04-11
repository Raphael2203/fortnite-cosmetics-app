from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from sqlalchemy import DateTime, String, Integer, func

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    vbucks: Mapped[int] = mapped_column(Integer, default=10000)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    
    purchases: Mapped[list["Purchase"]] = relationship(
        "Purchase",
        back_populates="user", 
        lazy="selectin"
        )


from ..purchases.models import Purchase