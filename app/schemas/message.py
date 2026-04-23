from datetime import datetime

from pydantic import BaseModel

class MessageBase(BaseModel):
    content: str
    role: str
    profile_id: int

class MessageCreate(MessageBase):
    pass

class MessageUpdate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True