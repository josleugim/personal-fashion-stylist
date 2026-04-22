from fastapi import APIRouter, Depends, HTTPException, Request, Response, Cookie, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate
from app.utils.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app import crud

router = APIRouter()


def _is_mobile_client(request: Request) -> bool:
    user_agent = request.headers.get("user-agent", "").lower()
    x_client = request.headers.get("x-client-type", "").lower()
    return "dart" in user_agent or x_client == "mobile"


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * settings.JWT_ACCESS_TOKEN_EXPIRE,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24 * settings.JWT_REFRESH_TOKEN_EXPIRE,
    )


@router.post("/login")
async def login(
    credentials: LoginRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.user.get_user_by_email(db, credentials.email)
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    payload = {"sub": str(user.id)}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    if _is_mobile_client(request):
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    _set_auth_cookies(response, access_token, refresh_token)
    return { "message": "Login successful", "user_id": user.id }


@router.post("/refresh")
async def refresh(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    refresh_token: str = Cookie(default=None),
):
    # Mobile clients send the refresh token in the request body
    if _is_mobile_client(request):
        body = await request.json()
        refresh_token = body.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    user_id = int(payload["sub"])
    user = await crud.user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    new_payload = {"sub": str(user.id)}
    new_access_token = create_access_token(new_payload)
    new_refresh_token = create_refresh_token(new_payload)

    if _is_mobile_client(request):
        return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)

    _set_auth_cookies(response, new_access_token, new_refresh_token)
    return {"message": "Token refreshed"}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_exists = await crud.user.get_user_by_email(db, user.email)

    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await crud.user.create_user(db, user)