from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.brand import Brand

async def get_brands(db: AsyncSession) -> list[Brand]:
    result = await db.execute(select(Brand).order_by(Brand.name))
    return result.scalars().all()