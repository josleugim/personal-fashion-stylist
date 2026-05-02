from app.models.wardrobe import Wardrobe
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

async def create(db: AsyncSession, profile_id: int, image_data: dict, ai_data: dict, user_data: dict) -> Wardrobe:
    item = Wardrobe(
        # From GCS upload
        image_filename = image_data["image_filename"],
        image_url      = image_data["image_url"],
        thumbnail_url  = image_data.get("thumbnail_url"),
        # From AI analysis
        category       = ai_data.get("category"),
        subcategory    = ai_data.get("subcategory"),
        color          = ai_data.get("color"),
        pattern        = ai_data.get("pattern"),
        style_tags     = ai_data.get("style_tags"),
        occasion_tags  = ai_data.get("occasion_tags"),
        season         = ai_data.get("season"),
        fabric         = ai_data.get("fabric"),
        ai_description = ai_data.get("ai_description"),
        ai_attributes  = ai_data if ai_data else None,
        # From user (optional)
        profile_id=profile_id,
        name           = user_data.get("name"),
        brand          = user_data.get("brand"),
        notes          = user_data.get("notes"),
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

async def get_by_user(db: AsyncSession, profile_id: int, skip: int = 0, limit: int = 20) -> list:
    result = await db.execute(
        select(Wardrobe)
        .filter(Wardrobe.profile_id == profile_id, Wardrobe.is_active == True)
        .order_by(Wardrobe.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_by_id(db: AsyncSession, item_id: UUID, profile_id: int) -> type[Wardrobe] | None:
    result = await db.execute(
        select(Wardrobe)
        .filter(Wardrobe.id == item_id, Wardrobe.profile_id == profile_id)
    )
    return result.scalar_one_or_none()

async def delete(db: AsyncSession, item_id: UUID, profile_id: int) -> bool:
    item = await get_by_id(db, item_id, profile_id)
    if not item:
        return False
    item.is_active = False
    await db.commit()
    return True