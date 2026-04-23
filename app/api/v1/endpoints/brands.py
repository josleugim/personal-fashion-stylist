from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.brand import BrandResponse, BrandCreate
from app import crud

router = APIRouter()

@router.get("/", response_model=list[BrandResponse])
async def get_brands(db: AsyncSession = Depends(get_db)):
    return await crud.brand.get_brands(db)

@router.post("/", response_model=BrandResponse, status_code=201)
async def create_brand(brand: BrandCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.brand.create_brand(db, brand)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Brand already exists")