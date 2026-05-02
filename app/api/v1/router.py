from fastapi import APIRouter, Depends
from app.api.v1.endpoints import (users, styles, body_type, messages, suggest_outfits, profiles, wardrobes, auth,
                                  brands, skin_tones, outfit_suggestions)
from app.api.deps import get_current_user

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

_auth_dep = [Depends(get_current_user)]
api_router.include_router(users.router, prefix="/users", tags=["users"], dependencies=_auth_dep)
api_router.include_router(styles.router, prefix="/styles", tags=["styles"], dependencies=_auth_dep)
api_router.include_router(body_type.router, prefix="/body-types", tags=["body-types"], dependencies=_auth_dep)
api_router.include_router(messages.router, prefix="/messages", tags=["messages"], dependencies=_auth_dep)
api_router.include_router(suggest_outfits.router, prefix="/suggest-outfits", tags=["suggest-outfits"], dependencies=_auth_dep)
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"], dependencies=_auth_dep)
api_router.include_router(wardrobes.router, prefix="/wardrobes", tags=["wardrobes"], dependencies=_auth_dep)
api_router.include_router(brands.router, prefix="/brands", tags=["brands"], dependencies=_auth_dep)
api_router.include_router(skin_tones.router, prefix="/skin-tones", tags=["skin-tones"], dependencies=_auth_dep)
api_router.include_router(outfit_suggestions.router, prefix="/outfit-suggestions", tags=["outfit-suggestions"], dependencies=_auth_dep)