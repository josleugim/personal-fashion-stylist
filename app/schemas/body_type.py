from pydantic import BaseModel
from fastapi import Form, UploadFile, File


class BodyTypeBase(BaseModel):
    name: str
    description: str
    image_url: str
    thumbnail_url: str
    is_active: bool = True

class BodyTypeCreate(BodyTypeBase):
    name: str = Form(...)
    description: str = Form(...)
    file: UploadFile = File(...)


class BodyTypeUpdate(BodyTypeBase):
    pass

class BodyTypeResponse(BodyTypeBase):
    id: int
    name: str
    description: str
    image_url: str
    thumbnail_url: str
    is_active: bool

    class Config:
        from_attributes = True