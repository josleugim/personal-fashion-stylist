from pydantic import BaseModel
from datetime import datetime

class BrandBase(BaseModel):
    name: str
    category: str
    tier: str
    origin: str

class BrandCreate(BrandBase):
    pass

class BrandUpdate(BrandBase):
    pass

class BrandResponse(BrandBase):
    id: int
    category: str
    tier: str
    origin: str
    created_at: datetime

    class Config:
        from_attributes = True