from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.message import Message
from app.models.profile import Profile
from app.schemas.suggest_outfit import SuggestOutfitResponse, SuggestOutfitRequest
from app.schemas.message import MessageCreate
from app.crud import user as crud_user         # adjust to your crud module names
from app.crud import profile as crud_profile
from app.crud import message as crud_message
from app.models.user import User
from app.core.claude import build_system_prompt, call_claude

router = APIRouter()

@router.post("/", response_model=SuggestOutfitResponse, status_code=200)
async def suggest_outfit(
        payload: SuggestOutfitRequest,
        db: AsyncSession = Depends(get_db)
):
    # ── 1. Fetch user data from existing models ──────────────────
    user: User | None = await crud_user.get_user(db, payload.user_id)
    profile: Profile | None = await crud_profile.get_profile(db, payload.profile_id)

    if not user or not profile:
        raise HTTPException(status_code=404, detail="User or profile not found.")

    if not payload.message and not payload.image_base64:
        raise HTTPException(status_code=400, detail="message or image_base64 is required.")

    # ── 2. Build user profile dict for prompt ────────────────────
    user_profile = {
        "name": user.first_name,
        "primary_style": profile.styles if profile.styles else "minimalist",
        # "gender_expression": profile.gender_expression,
        "palette_preference": profile.favorite_colors or [],
        "avoid_colors": profile.colors_to_avoid or [],
        "body_notes": profile.body_types if profile.body_types else "",
        "budget": profile.budget or "mid",
        "location": profile.location or "",
        "occasion": payload.occasion,
        # "wardrobe_items": profile.wardrobe_items or [],
        "weather": payload.weather or "",
    }

    # ── 3. Fetch last 10 messages for conversation history ───────
    recent_messages: list[Message] = await crud_message.get_recent_by_user(db, payload.user_id, limit=10)
    history = [{"role": m.role, "content": m.content} for m in recent_messages]

    # ── 4. Append current user message to history ────────────────
    current_message = payload.message or "[photo upload]"
    history.append({"role": "user", "content": current_message})

    # ── 5. Call Claude ───────────────────────────────────────────
    system_prompt = build_system_prompt(user_profile)
    try:
        reply = await call_claude(
            system_prompt=system_prompt,
            messages=history,
            image_base64=payload.image_base64
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Claude API error: {str(e)}")

    # ── 6. Save exchange to message model ────────────────────────
    await crud_message.create_message(db, MessageCreate(profile_id=payload.user_id, role="user", content=current_message))
    await crud_message.create_message(db, MessageCreate(profile_id=payload.user_id, role="assistant", content=reply))

    return SuggestOutfitResponse(success=True, reply=reply)