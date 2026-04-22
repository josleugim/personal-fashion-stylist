from typing import Optional
from pydantic import BaseModel


class BodyTypeBase(BaseModel):
    name: str
    description: str
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_active: bool = True

class BodyTypeCreate(BodyTypeBase):
    pass


class BodyTypeUpdate(BodyTypeBase):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class BodyTypeResponse(BodyTypeBase):
    id: int
    name: str
    description: str
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True