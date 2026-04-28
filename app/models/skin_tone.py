from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.profile import Profile

class SkinTone(Base):
    __tablename__ = "skin_tones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hex: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    profiles: Mapped[List["Profile"]] = relationship(back_populates="skin_tone")