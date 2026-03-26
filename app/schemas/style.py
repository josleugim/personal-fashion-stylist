from pydantic import BaseModel
from app.enums.style import StrictnessLevel

class StyleBase(BaseModel):
    name: str
    description: str
    strictness: StrictnessLevel
    palette: list[str] | None = None
    avoid: list[str] | None = None
    is_active: bool = True

class StyleCreate(StyleBase):
    pass

class StyleUpdate(StyleBase):
    pass

class StyleResponse(StyleBase):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True