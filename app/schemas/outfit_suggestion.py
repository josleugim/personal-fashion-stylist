import uuid
from datetime import datetime

from pydantic import BaseModel


class OutfitSuggestionBase(BaseModel):
    profile_id: int
    reply: str
    wardrobe_item_ids: list[uuid.UUID] | None = None

class OutfitSuggestionCreate(OutfitSuggestionBase):
    pass

class OutfitSuggestionUpdate(OutfitSuggestionBase):
    pass

class OutfitSuggestionResponse(OutfitSuggestionBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True