from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.brand import Brand
from app.models.profile import Profile
from app.models.style import Style
from app.models.body_type import BodyType
from app.schemas.profile import ProfileCreate

async def get_profile_by_user_id(db: AsyncSession, user_id: int) -> Profile | None:
    result = await db.execute(
        select(Profile)
        .where(Profile.user_id == user_id)
        .options(selectinload(Profile.styles), selectinload(Profile.body_types), selectinload(Profile.wardrobes), selectinload(Profile.favorite_brands))
    )
    return result.scalar_one_or_none()

async def create_profile(db: AsyncSession, profile: ProfileCreate) -> Profile:
    styles = (await db.execute(select(Style).where(Style.id.in_(profile.style_ids)))).scalars().all()
    body_types = (await db.execute(select(BodyType).where(BodyType.id.in_(profile.body_type_ids)))).scalars().all()
    favorite_brands = (await db.execute(select(Brand).where(Brand.id.in_(profile.favorite_brand_ids)))).scalars().all()

    db_profile = Profile(
        user_id=profile.user_id,
        styles=styles,
        body_types=body_types,
        favorite_brands=favorite_brands,
        fit_notes=profile.fit_notes,
        favorite_colors=profile.favorite_colors,
        colors_to_avoid=profile.colors_to_avoid,
        budget=profile.budget,
        logo_tolerance=profile.logo_tolerance,
        hobbies=profile.hobbies,
        sports=profile.sports,
        age=profile.age,
        location=profile.location,
        height=profile.height,
        gender=profile.gender
    )
    db.add(db_profile)
    await db.flush()
    return await get_profile_by_user_id(db, db_profile.user_id)
    