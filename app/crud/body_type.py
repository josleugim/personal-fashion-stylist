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

async def create_body_type(db: AsyncSession, body_type: BodyTypeCreate, image_data: dict) -> BodyType:
    db_body_type = BodyType(
        name=body_type.name,
        description=body_type.description,
        image_filename=image_data["image_filename"],
        image_url=image_data["image_url"],
        thumbnail_url=image_data["thumbnail_url"]
    )
    db.add(db_body_type)
    await db.flush()
    await db.refresh(db_body_type)
    return db_body_type

async def put_body_type(db: AsyncSession, body_type_id: int, body_type: BodyTypeUpdate, image_data: dict | None) -> BodyType | None:
    db_body_type = await get_body_type_by_id(db, body_type_id)
    if db_body_type is None:
        return None

    if body_type.name is not None:
        db_body_type.name = body_type.name
    if body_type.description is not None:
        db_body_type.description = body_type.description
    if body_type.is_active is not None:
        db_body_type.is_active = body_type.is_active
    if image_data is not None:
        db_body_type.image_filename = image_data["image_filename"]
        db_body_type.image_url = image_data["image_url"]
        db_body_type.thumbnail_url = image_data["thumbnail_url"]

    await db.flush()
    await db.refresh(db_body_type)
    return db_body_type
