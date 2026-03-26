from pydantic import BaseModel
from typing import List
from app.schemas.style import StyleResponse
from app.schemas.body_type import BodyTypeResponse

class ProfileBase(BaseModel):
    fit_notes: str | None = None
    favorite_colors: str | None = None
    colors_to_avoid: str | None = None

class ProfileCreate(ProfileBase):
    fit_notes: str | None = None
    favorite_colors: str | None = None
    colors_to_avoid: str | None = None
    style_ids: List[int] = []
    body_type_ids: List[int] = []

class ProfileUpdate(ProfileBase):
    fit_notes: str | None = None
    favorite_colors: str | None = None
    colors_to_avoid: str | None = None
    style_ids: List[int] | None = None
    body_type_ids: List[int] | None = None

class ProfileResponse(ProfileBase):
    id: int
    fit_notes: str | None = None
    favorite_colors: str | None = None
    colors_to_avoid: str | None = None
    styles: List[StyleResponse] = []
    body_types: List[BodyTypeResponse] = []

    class Config:
        from_attributes = True