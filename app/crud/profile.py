from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate

async def get_profile(db: AsyncSession, profile_id: int) -> Profile | None:
    result = await db.execute(select(Profile).where(Profile.id == profile_id))
    return result.scalar_one_or_none()

async def create_profile(db: AsyncSession, profile: ProfileCreate) -> Profile:
    db_profile = Profile(
        user_id=profile.user_id,
        fit_notes=profile.fit_notes,
        favorite_colors=profile.favorite_colors,
        colors_to_avoid=profile.colors_to_avoid,
    )
    db.add(db_profile)
    await db.flush()
    await db.refresh(db_profile)
    return db_profile
    