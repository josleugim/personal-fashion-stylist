from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel


class Wardrobe(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    notes: Optional[str] = None
    profile_id: int

class WardrobeResponse(BaseModel):
    id:            UUID
    profile_id:    int
    image_url:     str
    thumbnail_url: Optional[str]
    name:          Optional[str]
    category:      Optional[str]
    subcategory:   Optional[str]
    color:         Optional[List[str]]
    pattern:       Optional[str]
    style_tags:    Optional[List[str]]
    occasion_tags: Optional[List[str]]
    season:        Optional[List[str]]
    fabric:        Optional[str]
    brand:         Optional[str]
    ai_description: Optional[str]
    is_favorite:   bool
    times_worn:    int
    created_at:    datetime

    class Config:
        from_attributes = True