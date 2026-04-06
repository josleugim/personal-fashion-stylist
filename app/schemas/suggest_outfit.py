from pydantic import BaseModel
from typing import Optional

class SuggestOutfitRequest(BaseModel):
    user_id: int
    profile_id: int
    message: Optional[str] = None
    image_base64: Optional[str] = None
    occasion: Optional[str] = None
    weather: Optional[str] = None

class SuggestOutfitResponse(BaseModel):
    success: bool
    reply: str