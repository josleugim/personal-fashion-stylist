from pydantic import BaseModel
from typing import List
from app.schemas.style import StyleResponse
from app.schemas.body_type import BodyTypeResponse


class ProfileBase(BaseModel):
    user_id: int
    style_ids: List[int] = []
    body_type_ids: List[int] = []
    fit_notes: str | None = None
    favorite_colors: List[str] = []
    colors_to_avoid: List[str] = []
    budget: str | None = None
    logo_tolerance: str | None = None
    hobbies: List[str] | None = None
    sports: List[str] | None = None
    age: int | None = None
    height: int | None = None

class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    styles: List[StyleResponse] = []
    body_types: List[BodyTypeResponse] = []
    fit_notes: str | None = None
    favorite_colors: List[str] = []
    colors_to_avoid: List[str] = []
    budget: str | None = None
    logo_tolerance: str | None = None
    hobbies: List[str] | None = None
    sports: List[str] | None = None
    age: int | None = None
    height: int | None = None

    class Config:
        from_attributes = True