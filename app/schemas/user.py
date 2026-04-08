from __future__ import annotations
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: str
    last_name: str | None = None
    email: EmailStr


class UserCreate(UserBase):
    pass
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class UserResponse(UserBase):
    id: int
    profile: ProfileResponse | None = None

    class Config:
        from_attributes = True


from app.schemas.profile import ProfileResponse  # noqa: E402
UserResponse.model_rebuild()