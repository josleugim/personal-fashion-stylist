from pydantic import BaseModel

class StyleBase(BaseModel):
    name: str
    description: str
    is_active: bool = True

class StyleCreate(StyleBase):
    pass

class StyleUpdate(StyleBase):
    pass

class StyleResponse(StyleBase):
    id: int

    class Config:
        from_attributes = True