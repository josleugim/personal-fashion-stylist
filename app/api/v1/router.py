from fastapi import APIRouter
from app.api.v1.endpoints import (users, styles, body_type, messages, suggest_outfits, profiles, wardrobes, auth,
                                  brands, skin_tones, outfit_suggestions)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(styles.router, prefix="/styles", tags=["styles"])
api_router.include_router(body_type.router, prefix="/body-types", tags=["body-types"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(suggest_outfits.router, prefix="/suggest-outfits", tags=["suggest-outfits"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(wardrobes.router, prefix="/wardrobes", tags=["wardrobes"])
api_router.include_router(brands.router, prefix="/brands", tags=["brands"])
api_router.include_router(skin_tones.router, prefix="/skin-tones", tags=["skin-tones"])
api_router.include_router(outfit_suggestions.router, prefix="/outfit-suggestions", tags=["outfit-suggestions"])