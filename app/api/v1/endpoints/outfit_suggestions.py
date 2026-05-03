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
        page: int = 1,
        page_size: int = 5,
        db: AsyncSession = Depends(get_db),
        current_profile: Profile = Depends(get_current_profile)
):
    if current_profile.id != profile_id:
        raise HTTPException(status_code=403, detail="Access denied")

    if page < 1:
        raise HTTPException(status_code=400, detail="page must be >= 1")
    if not (1 <= page_size <= 100):
        raise HTTPException(status_code=400, detail="page_size must be between 1 and 100")

    skip = (page - 1) * page_size
    return await crud.outfit_suggestion.get_outfit_suggestions(db, profile_id, skip=skip, limit=page_size)