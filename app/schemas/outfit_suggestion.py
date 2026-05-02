import uuid
from datetime import datetime

from pydantic import BaseModel


class WardrobeItemSummary(BaseModel):
    id: uuid.UUID
    brand: str | None = None
    thumbnail_url: str | None = None
    color: list[str] | None = None

    class Config:
        from_attributes = True


class OutfitSuggestionBase(BaseModel):
    profile_id: int
    reply: str
    wardrobe_item_ids: list[uuid.UUID] | None = None

class OutfitSuggestionCreate(OutfitSuggestionBase):
    pass

class OutfitSuggestionUpdate(OutfitSuggestionBase):
    pass

class OutfitSuggestionResponse(BaseModel):
    id: uuid.UUID
    profile_id: int
    reply: str
    wardrobe_items: list[WardrobeItemSummary] | None = None
    color: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True