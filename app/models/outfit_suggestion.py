import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.profile import Profile

class OutfitSuggestion(Base):
    __tablename__ = "outfit_suggestions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    profile: Mapped["Profile"] = relationship(back_populates="outfit_suggestions")
    reply: Mapped[str] = mapped_column(Text, nullable=False)
    wardrobe_item_ids: Mapped[List[uuid.UUID] | None] = mapped_column(ARRAY(UUID(as_uuid=True)), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)