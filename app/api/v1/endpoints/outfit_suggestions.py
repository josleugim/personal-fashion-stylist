from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.outfit_suggestion import OutfitSuggestionResponse
from app import crud

router = APIRouter()

@router.get("/{profile_id}", response_model=list[OutfitSuggestionResponse])
async def get_outfit_suggestions_by_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.outfit_suggestion.get_outfit_suggestions(db, profile_id)