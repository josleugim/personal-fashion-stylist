from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String, DateTime, Table, Column
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum

from app.db.base import Base
from app.models.style import Style
from app.models.body_type import BodyType
from app.models.brand import Brand
from app.enums.profile import LogoTolerance
from app.models.skin_tone import SkinTone

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.message import Message
    from app.models.wardrobe import Wardrobe
    from app.models.outfit_suggestion import OutfitSuggestion


profile_styles = Table(
    "profile_styles",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True),
    Column("style_id", Integer, ForeignKey("styles.id", ondelete="CASCADE"), primary_key=True),
)

profile_body_types = Table(
    "profile_body_types",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True),
    Column("body_type_id", Integer, ForeignKey("body_types.id", ondelete="CASCADE"), primary_key=True),
)

profile_brands = Table(
    "profile_brands",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True),
    Column("brand_id", UUID(as_uuid=True), ForeignKey("brands.id", ondelete="CASCADE"), primary_key=True),
)


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    user: Mapped["User"] = relationship(back_populates="profile", uselist=False)
    styles: Mapped[List["Style"]] = relationship(secondary=profile_styles, back_populates="profiles")
    body_types: Mapped[List["BodyType"]] = relationship(secondary=profile_body_types, back_populates="profiles")
    favorite_brands: Mapped[List["Brand"]] = relationship(secondary=profile_brands, back_populates="profiles")
    messages: Mapped[List["Message"]] = relationship(back_populates="profile")
    wardrobes: Mapped[List["Wardrobe"]] = relationship(back_populates="profile")
    outfit_suggestions: Mapped[List["OutfitSuggestion"]] = relationship(back_populates="profile")
    fit_notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    favorite_colors: Mapped[List[str] | None] = mapped_column(ARRAY(String), nullable=True)
    colors_to_avoid: Mapped[List[str] | None] = mapped_column(ARRAY(String), nullable=True)
    budget: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location: Mapped[str | None] = mapped_column(String(100), nullable=True)
    logo_tolerance: Mapped[str | None] = mapped_column(SAEnum(LogoTolerance), nullable=True)
    hobbies: Mapped[List[str] | None] = mapped_column(ARRAY(String), nullable=True)
    sports: Mapped[List[str] | None] = mapped_column(ARRAY(String), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(255), nullable=True)
    skin_tone_id: Mapped[int | None] = mapped_column(ForeignKey("skin_tones.id", ondelete="SET NULL"), nullable=True)
    skin_tone: Mapped["SkinTone | None"] = relationship(back_populates="profiles")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
