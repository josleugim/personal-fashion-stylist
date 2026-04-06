from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.message import Message
from app.schemas.message import MessageCreate

async def get_messages(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Message]:
    result = await db.execute(select(Message).offset(skip).limit(limit))
    return result.scalars().all()

async def create_message(db: AsyncSession, message: MessageCreate) -> Message:
    db_message = Message(
        role=message.role,
        content=message.content
    )
    db.add(db_message)
    await db.flush()
    await db.refresh(db_message)
    return db_message