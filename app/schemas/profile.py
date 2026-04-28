from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import List

from app.schemas.style import StyleResponse
from app.schemas.body_type import BodyTypeResponse
from app.schemas.brand import BrandResponse
from app.schemas.skin_tone import SkinToneResponse


class ProfileBase(BaseModel):
    user_id: int
    style_ids: List[int] = []
    body_type_ids: List[int] = []
    favorite_brand_ids: List[UUID] = []
    fit_notes: str | None = None
    favorite_colors: List[str] = []
    colors_to_avoid: List[str] = []
    budget: str | None = None
    location: str | None = None
    logo_tolerance: str | None = None
    hobbies: List[str] | None = None
    sports: List[str] | None = None
    age: int | None = None
    height: int | None = None
    gender: str | None = None
    skin_tone_id: int | None = None

class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    styles: List[StyleResponse] = []
    body_types: List[BodyTypeResponse] = []
    favorite_brands: List[BrandResponse] = []
    fit_notes: str | None = None
    favorite_colors: List[str] = []
    colors_to_avoid: List[str] = []
    budget: str | None = None
    location: str | None = None
    logo_tolerance: str | None = None
    hobbies: List[str] | None = None
    sports: List[str] | None = None
    age: int | None = None
    height: int | None = None
    gender: str | None = None
    skin_tone_id: int | None = None
    skin_tone: SkinToneResponse | None = None
    created_at: datetime

    class Config:
        from_attributes = True