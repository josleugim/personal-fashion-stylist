from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.style import Style
from app.schemas.style import StyleCreate, StyleUpdate

async def get_style(db: AsyncSession, style_id: int) -> Style | None:
    result = await db.execute(select(Style).where(Style.id == style_id))
    return result.scalar_one_or_none()

async def get_styles(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Style]:
    result = await db.execute(select(Style).offset(skip).limit(limit))
    return result.scalars().all()

async def create_style(db: AsyncSession, style: StyleCreate) -> Style:
    db_style = Style(
        name=style.name,
        description=style.description,
    )
    db.add(db_style)
    await db.flush()
    await db.refresh(db_style)
    return db_style

async def update_style(db: AsyncSession, db_style: Style, style: StyleUpdate) -> Style:
    update_data = style.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_style, field, value)
    db.add(db_style)
    await db.flush()
    await db.refresh(db_style)
    return db_style