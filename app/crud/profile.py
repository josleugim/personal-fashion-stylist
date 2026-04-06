from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.profile import Profile
from app.models.style import Style
from app.models.body_type import BodyType
from app.schemas.profile import ProfileCreate

async def get_profile(db: AsyncSession, profile_id: int) -> Profile | None:
    result = await db.execute(select(Profile).where(Profile.id == profile_id))
    return result.scalar_one_or_none()

async def create_profile(db: AsyncSession, profile: ProfileCreate) -> Profile:
    styles = (await db.execute(select(Style).where(Style.id.in_(profile.style_ids)))).scalars().all()
    body_types = (await db.execute(select(BodyType).where(BodyType.id.in_(profile.body_type_ids)))).scalars().all()

    db_profile = Profile(
        user_id=profile.user_id,
        styles=styles,
        body_types=body_types,
        fit_notes=profile.fit_notes,
        favorite_colors=profile.favorite_colors,
        colors_to_avoid=profile.colors_to_avoid,
        budget=profile.budget,
        logo_tolerance=profile.logo_tolerance,
    )
    db.add(db_profile)
    await db.flush()
    await db.refresh(db_profile)
    return db_profile
    