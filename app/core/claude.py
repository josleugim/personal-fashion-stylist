import httpx
import json
from app.core.config import settings

def build_system_prompt(user_profile: dict) -> str:
    style = user_profile.get("primary_style", "minimalist")
    name = user_profile.get("name", "the user")
    palette = ", ".join(user_profile.get("palette_preference", []))
    avoid = ", ".join(user_profile.get("avoid_colors", []))
    body_notes = user_profile.get("body_notes", "none provided")
    budget = user_profile.get("budget", "mid")
    location = user_profile.get("location", "")
    occasions = ", ".join(user_profile.get("occasions", []))
    wardrobe = ", ".join(user_profile.get("wardrobe_items", []))

    budget_guidance = {
        "low": "Suggest accessible brands (Zara, H&M, ASOS, Mango).",
        "mid": "Suggest mid-range brands (COS, Arket, Club Monaco, Banana Republic).",
        "luxury": "Suggest investment pieces (The Row, Totême, Loro Piana)."
    }.get(budget, "")

    return f"""
    You are a personal fashion stylist.
    Suggest outfit combinations tailored to the user's style, wardrobe, and occasion.

    USER PROFILE
    ─────────────────────────────────
    Name: {name}
    Location: {location}
    Primary style: {style}
    Preferred colors: {palette}
    Colors to avoid: {avoid}
    Body/fit notes: {body_notes}
    Typical occasions: {occasions}
    Wardrobe items: {wardrobe}

    BUDGET GUIDANCE
    ─────────────────────────────────
    {budget_guidance}

    RESPONSE RULES
    ─────────────────────────────────
    1. Always suggest COMPLETE outfits (top + bottom + shoes + optional accessory).
    2. Briefly explain WHY each outfit works for this user's style.
    3. If a photo is provided, identify the piece and suggest 2–3 outfits using it.
    4. Keep responses concise and conversational — this is a mobile app.
    5. Format each outfit like this:

       **[Outfit name]**
       • Top: [item]
       • Bottom: [item]
       • Shoes: [item]
       • Accessory: [item] (optional)
       💡 [1-sentence why it works]
    """.strip()

async def call_claude(system_prompt: str, messages: list, image_base64: str = None):
    if image_base64:
        user_content = [
            {"type": "image", "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": image_base64
            }},
            {"type": "text", "text": messages[-1]["content"]}
        ]
        messages = messages[:-1] + [{"role": "user", "content": user_content}]

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "system": system_prompt,
        "tools": [{"type": "web_search_20250305", "name": "web_search"}],
        "messages": messages
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        response.raise_for_status()
        data = response.json()

        # Extract text blocks (may also contain tool_use blocks)
        return "\n".join(
            block["text"]
            for block in data.get("content", [])
            if block.get("type") == "text"
        )