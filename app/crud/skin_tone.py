from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.skin_tone import SkinTone
from app.schemas.skin_tone import SkinToneCreate, SkinToneResponse

async def create_skin_tone(db: AsyncSession, skin_tone: SkinToneCreate) -> SkinTone:
    db_skin_tone = SkinTone(
        name=skin_tone.name,
        hex=skin_tone.hex
    )
    db.add(db_skin_tone)
    await db.flush()
    await db.refresh(db_skin_tone)

    return db_skin_tone

async def get_skin_tones(db: AsyncSession) -> list[SkinToneResponse]:
    result = await db.execute(select(SkinTone).order_by(SkinTone.hex))

    return result.scalars().all()