from datetime import datetime
from pydantic import BaseModel


class SkinToneBase(BaseModel):
    id: int
    name: str
    hex: str

class SkinToneCreate(SkinToneBase):
    pass

class SkinToneUpdate(SkinToneBase):
    pass

class SkinToneResponse(SkinToneBase):
    created_at: datetime

    class Config:
        from_attributes = True