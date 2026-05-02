from fastapi import Request, Depends, Cookie, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.utils.security import decode_token
from app import crud
from app.crud import profile as crud_profile

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db), access_token: str = Cookie(default=None)):
    # Mobile: Bearer token in Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    else:
        token = access_token # Web: cookie

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user = await crud.user.get_user(db, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

async def get_current_profile(current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    profile = await crud_profile.get_profile_by_user_id(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found for this user")
    return profile