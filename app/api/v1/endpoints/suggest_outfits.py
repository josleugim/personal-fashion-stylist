from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.message import Message
from app.models.profile import Profile
from app.schemas.suggest_outfit import SuggestOutfitResponse, SuggestOutfitRequest
from app.schemas.message import MessageCreate
from app.crud import user as crud_user
from app.crud import profile as crud_profile
from app.crud import message as crud_message
from app.crud import wardrobe as crud_wardrobe
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
    profile: Profile | None = await crud_profile.get_profile_by_user_id(db, payload.user_id)

    if not user or not profile:
        raise HTTPException(status_code=404, detail="User or profile not found.")

    if not payload.message and not payload.image_base64:
        raise HTTPException(status_code=400, detail="message or image_base64 is required.")

    # ── Fetch wardrobe items ─────────────────────────────────────
    wardrobe_items = await crud_wardrobe.get_by_user(db, profile.id)
    wardrobe_dicts = [
        {
            "id": str(item.id),
            "name": item.name,
            "brand": item.brand,
            "color": item.color or [],
            "category": item.category,
            "subcategory": item.subcategory,
            "image_url": item.image_url,
            "thumbnail_url": item.thumbnail_url,
            "ai_description": item.ai_description,
        }
        for item in wardrobe_items
    ]

    # ── 2. Build user profile dict for prompt ────────────────────
    user_profile = {
        "name": user.first_name,
        "primary_style": ", ".join(s.name for s in profile.styles) if profile.styles else "minimalist",
        "gender_expression": profile.gender,
        "palette_preference": profile.favorite_colors or [],
        "avoid_colors": profile.colors_to_avoid or [],
        "body_notes": ", ".join(bt.name for bt in profile.body_types) if profile.body_types else "",
        "budget": profile.budget or "mid",
        "location": profile.location or "",
        "logo_tolerance": profile.logo_tolerance.value if profile.logo_tolerance else "",
        "hobbies": profile.hobbies or [],
        "sports": profile.sports or [],
        "age": profile.age or None,
        "height": profile.height or None,
        "occasion": [payload.occasion] if payload.occasion else [],
        "wardrobe": [
            f"{item['brand']} {item['name'] or item['subcategory'] or item['category']}"
            for item in wardrobe_dicts
        ],
        "weather": payload.weather or "",
        "skin_tone": f"{profile.skin_tone.name} ({profile.skin_tone.hex})" if profile.skin_tone else ""
    }

    # ── 3. Fetch last 10 messages for conversation history ───────
    recent_messages: list[Message] = await crud_message.get_recent_by_user(db, profile.id, limit=10)
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
            image_base64=payload.image_base64,
            wardrobe=wardrobe_dicts
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Claude API error: {str(e)}")

    # ── 6. Save exchange to message model ────────────────────────
    await crud_message.create_message(db, MessageCreate(profile_id=profile.id, role="user", content=current_message))
    await crud_message.create_message(db, MessageCreate(profile_id=profile.id, role="assistant", content=reply["reply"]))

    return SuggestOutfitResponse(success=True, reply=reply["reply"], wardrobe_references=reply["wardrobe_references"])