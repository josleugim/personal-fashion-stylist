import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.profile import Profile

class Wardrobe(Base):
    __tablename__ = "wardrobes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    profile = relationship("Profile", back_populates="wardrobes")
    # ── Image storage (Google Cloud Bucket) ─────────────────────
    image_filename = Column(String, nullable=False)  # original filename
    image_url = Column(String, nullable=False)  # public/signed GCS URL
    thumbnail_url = Column(String, nullable=True)  # smaller version for grid view

    # ── Classification ──────────────────────────────────────────
    category = Column(String, nullable=True)  # top, bottom, shoes, accessory, outerwear, bag
    subcategory = Column(String, nullable=True)  # t-shirt, jeans, sneakers, belt...

    # ── Attributes (for Claude outfit suggestions) ───────────────
    color = Column(ARRAY(String), nullable=True)  # ["white", "navy"] — multi-color items
    pattern = Column(String, nullable=True)  # solid, striped, plaid, floral, graphic
    style_tags = Column(ARRAY(String), nullable=True)  # ["minimalist", "casual", "streetwear"]
    occasion_tags = Column(ARRAY(String), nullable=True)  # ["office", "casual", "formal", "sport"]
    season = Column(ARRAY(String), nullable=True)  # ["spring", "summer", "fall", "winter"]
    fabric = Column(String, nullable=True)  # cotton, linen, wool, polyester...

    # ── Brand & product info ─────────────────────────────────────
    brand = Column(String, nullable=True)
    name = Column(String, nullable=True)  # user-given name e.g. "My white linen shirt"
    notes = Column(String, nullable=True)  # free text notes from user

    # ── Status & usage ──────────────────────────────────────────
    is_active = Column(Boolean, default=True)  # soft delete / archived items
    is_favorite = Column(Boolean, default=False)  # user-marked favorites
    times_worn = Column(Integer, default=0)  # wear counter
    last_worn_at = Column(DateTime, nullable=True)

    # ── AI-generated metadata ────────────────────────────────────
    ai_description = Column(String, nullable=True)  # Claude's description of the item from photo
    ai_attributes = Column(JSONB, nullable=True)  # raw AI analysis result for future use

    # ── Timestamps ──────────────────────────────────────────────
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
