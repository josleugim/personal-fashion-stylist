from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.body_type import BodyTypeCreate, BodyTypeUpdate, BodyTypeResponse
from app import crud

router = APIRouter()

@router.get("/", response_model=list[BodyTypeResponse])
async def get_all_body_types(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.body_type.get_body_types(db, skip=skip, limit=limit)

@router.post("/", response_model=BodyTypeResponse, status_code=201)
async def create_body_type(body_type: BodyTypeCreate, db: AsyncSession = Depends(get_db)):
    return await crud.body_type.create_body_type(db, body_type)