from fastapi import APIRouter
from app.api.v1.endpoints import users, styles, body_type, messages

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(styles.router, prefix="/styles", tags=["styles"])
api_router.include_router(body_type.router, prefix="/body-types", tags=["body-types"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])