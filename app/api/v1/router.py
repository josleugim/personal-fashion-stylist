from fastapi import APIRouter
from app.api.v1.endpoints import users, styles

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(styles.router, prefix="/styles", tags=["styles"])