import httpx
import json
from fastapi import HTTPException

from app.core.config import settings

def build_system_prompt(user_profile: dict) -> str:
    style = user_profile.get("primary_style", "minimalist")
    name = user_profile.get("name", "the user")
    palette = ", ".join(user_profile.get("palette_preference", []))
    avoid = ", ".join(user_profile.get("avoid_colors", []))
    body_notes = user_profile.get("body_notes", "none provided")
    budget = user_profile.get("budget", "mid")
    location = user_profile.get("location", "")
    occasion = ", ".join(user_profile.get("occasion", ""))
    wardrobe = ", ".join(user_profile.get("wardrobe", []))
    weather = user_profile.get("weather", "")

    budget_guidance = {
        "low": "Suggest accessible brands (Zara, H&M, ASOS, Mango).",
        "mid": "Suggest mid-range brands (COS, Arket, Club Monaco, Banana Republic).",
        "luxury": "Suggest investment pieces (The Row, Totême, Loro Piana)."
    }.get(budget, "")

    return f"""
    You are a personal fashion stylist.
    Suggest outfit combinations tailored to the user's style, wardrobe, and occasion.
    Always respond in the same language the user writes in.

    USER PROFILE
    ─────────────────────────────────
    Name: {name}
    Location: {location}
    Primary style: {style}
    Preferred colors: {palette}
    Colors to avoid: {avoid}
    Body/fit notes: {body_notes}
    Typical occasion: {occasion}
    Wardrobe items: {wardrobe}
    Weather: {weather}

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

async def call_claude(system_prompt: str, messages: list, image_base64: str = None, wardrobe: list = []) -> dict:
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

        # Sanitize messages
        messages = [m for m in messages if m.get("content")]
        while messages and messages[0]["role"] == "assistant":
            messages.pop(0)

    payload = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "system": system_prompt,
        "tools": [{"type": "web_search_20250305", "name": "web_search"}],
        "messages": messages
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01"
            },
            json=payload
        )
        if response.status_code != 200:
            print("Claude error body:", response.json())
            raise HTTPException(status_code=502, detail=response.json())

        response.raise_for_status()
        data = response.json()

        # Extract text blocks (may also contain tool_use blocks)
        reply_text = "\n".join(
            block["text"]
            for block in data.get("content", [])
            if block.get("type") == "text"
        )

        # ── Match wardrobe items mentioned in the reply ──────────────
        matched_items = _match_wardrobe_items(reply_text, wardrobe)

        return {
            "reply": reply_text,
            "wardrobe_references": matched_items
        }

async def analyze_wardrobe_item(image_base64: str, media_type: str = "image/jpeg") -> dict:
    payload = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 500,
        "system": """You are a fashion item analyzer. When given a clothing photo, 
        return ONLY a JSON object with no extra text.""",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image", "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": image_base64
                }},
                {"type": "text", "text": """Analyze this clothing item and return JSON:
                {
                  "category": "top|bottom|shoes|outerwear|accessory|bag|dress|activewear",
                  "subcategory": "t-shirt|jeans|sneakers|etc",
                  "color": ["primary color", "secondary color if any"],
                  "pattern": "solid|striped|plaid|floral|graphic|animal-print|etc",
                  "style_tags": ["minimalist", "casual", "streetwear", "etc — max 3"],
                  "occasion_tags": ["everyday", "office", "formal", "sport", "etc — max 3"],
                  "season": ["spring", "summer", "fall", "winter"],
                  "fabric": "cotton|linen|wool|denim|leather|synthetic|etc",
                  "ai_description": "One natural sentence describing this item"
                }"""}
            ]
        }]
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01"
            },
            json=payload
        )
        data = response.json()

    if "content" not in data:
        print(f"[Claude API error] {data}")
        return {}

    raw = data["content"][0]["text"]
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)

def _match_wardrobe_items(reply_text: str, wardrobe_items: list) -> list:
    """Find wardrobe items whose name or brand appears in Claude's reply."""
    reply_lower = reply_text.lower()
    matched = []

    for item in wardrobe_items:
        # Check if item name or brand is mentioned in the reply
        name_match  = item.get("name")  and item["name"].lower()  in reply_lower
        brand_match = item.get("brand") and item["brand"].lower() in reply_lower

        if name_match or brand_match:
            matched.append({
                "id":            str(item.get("id")),
                "name":          item.get("name"),
                "brand":         item.get("brand"),
                "category":      item.get("category"),
                "subcategory":   item.get("subcategory"),
                "image_url":     item.get("image_url"),
                "thumbnail_url": item.get("thumbnail_url"),
                "ai_description": item.get("ai_description"),
            })

    return matched