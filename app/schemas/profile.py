from pydantic import BaseModel
from typing import List

class ProfileBase(BaseModel):
    user_id: int
    style_ids: List[int] = []
    body_type_ids: List[int] = []
    fit_notes: str | None = None
    favorite_colors: List[str] = []
    colors_to_avoid: List[str] = []
    budget: str | None = None
    logo_tolerance: str | None = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    style_ids: List[int] = []
    body_type_ids: List[int] = []
    fit_notes: str | None = None
    favorite_colors: List[str] = []
    colors_to_avoid: List[str] = []
    budget: str | None = None
    logo_tolerance: str | None = None

    class Config:
        from_attributes = True