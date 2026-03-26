from pydantic import BaseModel

class BodyTypeBase(BaseModel):
    name: str
    description: str
    is_active: bool = True

class BodyTypeCreate(BodyTypeBase):
    pass

class BodyTypeUpdate(BodyTypeBase):
    pass

class BodyTypeResponse(BodyTypeBase):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True