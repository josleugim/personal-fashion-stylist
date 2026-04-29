from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.outfit_suggestion import OutfitSuggestion
from app.schemas.outfit_suggestion import OutfitSuggestionResponse, OutfitSuggestionCreate


async def get_outfit_suggestions(db: AsyncSession, profile_id: int) -> list[OutfitSuggestionResponse]:
    result = await db.execute(
        select(OutfitSuggestion)
        .where(OutfitSuggestion.profile_id == profile_id)
        .order_by(OutfitSuggestion.created_at)
    )
    return result.scalars().all()

async def create_outfit_suggestion(db: AsyncSession, outfit_suggestion: OutfitSuggestionCreate) -> OutfitSuggestion:
    db_outfit_suggestion = OutfitSuggestion(
        profile_id=outfit_suggestion.profile_id,
        reply=outfit_suggestion.reply,
        wardrobe_item_ids=outfit_suggestion.wardrobe_item_ids
    )
    db.add(db_outfit_suggestion)
    await db.flush()
    await db.refresh(db_outfit_suggestion)

    return db_outfit_suggestion