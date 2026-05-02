from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.outfit_suggestion import OutfitSuggestion
from app.models.wardrobe import Wardrobe
from app.schemas.outfit_suggestion import OutfitSuggestionResponse, OutfitSuggestionCreate, WardrobeItemSummary


async def get_outfit_suggestions(db: AsyncSession, profile_id: int) -> list[OutfitSuggestionResponse]:
    result = await db.execute(
        select(OutfitSuggestion)
        .where(OutfitSuggestion.profile_id == profile_id)
        .order_by(OutfitSuggestion.created_at)
    )
    suggestions = result.scalars().all()

    all_ids = {wid for s in suggestions if s.wardrobe_item_ids for wid in s.wardrobe_item_ids}

    wardrobe_map: dict = {}
    if all_ids:
        wardrobe_result = await db.execute(
            select(Wardrobe.id, Wardrobe.brand, Wardrobe.thumbnail_url, Wardrobe.color)
            .where(Wardrobe.id.in_(all_ids))
        )
        wardrobe_map = {
            row.id: WardrobeItemSummary(id=row.id, brand=row.brand, thumbnail_url=row.thumbnail_url, color=row.color)
            for row in wardrobe_result
        }

    return [
        OutfitSuggestionResponse(
            id=s.id,
            profile_id=s.profile_id,
            reply=s.reply,
            wardrobe_items=[wardrobe_map[wid] for wid in (s.wardrobe_item_ids or []) if wid in wardrobe_map] or None,
            created_at=s.created_at,
        )
        for s in suggestions
    ]

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