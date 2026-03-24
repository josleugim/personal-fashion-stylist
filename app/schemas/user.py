from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True