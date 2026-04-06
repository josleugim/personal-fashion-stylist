from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.message import MessageResponse, MessageCreate
from app import crud

router = APIRouter()

@router.get("/", response_model=list[MessageResponse])
async def get_messages(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.message.get_messages(db, skip=skip, limit=limit)

@router.post("/", response_model=MessageResponse, status_code=201)
async def create_message(message: MessageCreate, db: AsyncSession = Depends(get_db)):
    return await crud.message.create_message(db, message)