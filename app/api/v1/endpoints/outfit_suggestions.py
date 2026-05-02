from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.outfit_suggestion import OutfitSuggestionResponse
from app import crud
from app.api.deps import get_current_profile
from app.models.profile import Profile

router = APIRouter()

@router.get("/{profile_id}", response_model=list[OutfitSuggestionResponse])
async def get_outfit_suggestions_by_profile(
        profile_id: int,
        db: AsyncSession = Depends(get_db),
        current_profile: Profile = Depends(get_current_profile)
):
    if current_profile.id != profile_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return await crud.outfit_suggestion.get_outfit_suggestions(db, profile_id)