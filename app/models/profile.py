from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String, DateTime, Table, Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum

from app.db.base import Base
from app.models.style import Style
from app.models.body_type import BodyType
from app.enums.profile import LogoTolerance

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.message import Message


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
    messages: Mapped[List["Message"]] = relationship(back_populates="profile")
    fit_notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    favorite_colors: Mapped[List[str] | None] = mapped_column(ARRAY(String), nullable=True)
    colors_to_avoid: Mapped[List[str] | None] = mapped_column(ARRAY(String), nullable=True)
    budget: Mapped[str | None] = mapped_column(String(100), nullable=True)
    logo_tolerance: Mapped[str | None] = mapped_column(SAEnum(LogoTolerance), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
