from pydantic import BaseModel
from typing import Optional, List

class WardrobeReference(BaseModel):
    id: str
    name: Optional[str]
    brand: Optional[str]
    category: Optional[str]
    subcategory: Optional[str]
    image_url: str
    thumbnail_url: Optional[str]
    ai_description: Optional[str]

class SuggestOutfitRequest(BaseModel):
    user_id: int
    message: Optional[str] = None
    image_base64: Optional[str] = None
    occasion: Optional[str] = None
    weather: Optional[str] = None

class SuggestOutfitResponse(BaseModel):
    success: bool
    reply: str
    wardrobe_references: List[WardrobeReference] = []