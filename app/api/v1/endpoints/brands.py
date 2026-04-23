from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.brand import BrandResponse
from app import crud

router = APIRouter()

@router.get("/", response_model=list[BrandResponse])
async def get_brands(db: AsyncSession = Depends(get_db)):
    return await crud.brand.get_brands(db)