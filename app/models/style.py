from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import String, Integer, DateTime, Boolean, ARRAY, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum

from app.db.base import Base
from app.enums.style import StrictnessLevel

if TYPE_CHECKING:
    from app.models.profile import Profile


class Style(Base):
    __tablename__ = "styles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    strictness: Mapped[str] = mapped_column(SAEnum(StrictnessLevel), nullable=False)
    palette: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    avoid: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    profiles: Mapped[List["Profile"]] = relationship(secondary="profile_styles", back_populates="styles")