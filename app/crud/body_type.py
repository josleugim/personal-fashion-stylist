from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.body_type import BodyType
from app.schemas.body_type import BodyTypeCreate, BodyTypeUpdate

async def get_body_type_by_id(db: AsyncSession, body_type_id: int) -> BodyType | None:
    result = await db.execute(select(BodyType).where(BodyType.id == body_type_id))
    return result.scalar_one_or_none()

async def get_body_types(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[BodyType]:
    result = await db.execute(select(BodyType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_body_type(db: AsyncSession, body_type: BodyTypeCreate) -> BodyType:
    db_body_type = BodyType(
        name=body_type.name,
        description=body_type.description,
    )
    db.add(db_body_type)
    await db.flush()
    await db.refresh(db_body_type)
    return db_body_type
    
