from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.brand import Brand
from app.schemas.brand import BrandCreate, BrandResponse


async def get_brands(db: AsyncSession) -> list[BrandResponse]:
    result = await db.execute(select(Brand).order_by(Brand.name))
    return result.scalars().all()

async def create_brand(db: AsyncSession, brand: BrandCreate) -> Brand:
    db_brand = Brand(
        name=brand.name,
        category=brand.category,
        tier=brand.tier,
        origin=brand.origin
    )
    db.add(db_brand)
    await db.flush()
    await db.refresh(db_brand)
    return db_brand