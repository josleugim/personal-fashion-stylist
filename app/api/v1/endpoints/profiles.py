from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.profile import ProfileCreate, ProfileResponse
from app.db.session import get_db
from app import crud

router = APIRouter()

@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(profile: ProfileCreate, db: AsyncSession = Depends(get_db)):
    return await crud.profile.create_profile(db, profile)

@router.get("/{profile_id}", response_model=ProfileResponse, status_code=status.HTTP_200_OK)
async def get_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    profile = await crud.profile.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile