import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Boolean, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING, List

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.profile import Profile

class Wardrobe(Base):
    __tablename__ = "wardrobes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)
    profile: Mapped["Profile"] = relationship(back_populates="wardrobes")
    # ── Image storage (Google Cloud Bucket) ─────────────────────
    image_filename: Mapped[str] = mapped_column(String, nullable=False)  # original filename
    image_url: Mapped[str] = mapped_column(String, nullable=False) # public/signed GCS URL
    thumbnail_url: Mapped[str] = mapped_column(String, nullable=True) # smaller version for grid view
    # ── Classification ──────────────────────────────────────────
    category: Mapped[str] = mapped_column(String, nullable=True) # top, bottom, shoes, accessory, outerwear, bag
    subcategory: Mapped[str] = mapped_column(String, nullable=True) # t-shirt, jeans, sneakers, belt...
    # ── Attributes (for Claude outfit suggestions) ───────────────
    color: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True) # ["white", "navy"] — multi-color items
    pattern: Mapped[str] = mapped_column(String, nullable=True) # solid, striped, plaid, floral, graphic
    style_tags: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True) # ["minimalist", "casual", "streetwear"]
    occasion_tags: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True) # ["office", "casual", "formal", "sport"]
    season: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True) # ["spring", "summer", "fall", "winter"]
    fabric: Mapped[str] = mapped_column(String, nullable=True) # cotton, linen, wool, polyester...
    # ── Brand & product info ─────────────────────────────────────
    brand: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True) # user-given name e.g. "My white linen shirt"
    notes: Mapped[str] = mapped_column(String, nullable=True) # free text notes from user
    # ── Status & usage ──────────────────────────────────────────
    is_active: Mapped[bool] = mapped_column(Boolean, default=True) # soft delete / archived items
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=True) # user-marked favorites
    times_worn: Mapped[int] = mapped_column(default=0)
    last_worn_at: Mapped[datetime | None] = mapped_column(DateTime)

    # ── AI-generated metadata ────────────────────────────────────
    ai_description: Mapped[str | None] = mapped_column(String)
    ai_attributes: Mapped[dict | None] = mapped_column(JSONB)

    # ── Timestamps ──────────────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
