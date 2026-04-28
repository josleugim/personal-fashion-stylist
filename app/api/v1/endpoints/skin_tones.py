from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.skin_tone import SkinToneResponse, SkinToneCreate
from app import crud

router = APIRouter()

@router.get("/", response_model=list[SkinToneResponse])
async def get_skin_tones(db: AsyncSession = Depends(get_db)):
    return await crud.skin_tone.get_skin_tones(db=db)

@router.post('/', response_model=SkinToneResponse, status_code=201)
async def create_skin_tone(skin_tone: SkinToneCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.skin_tone.create_skin_tone(db, skin_tone)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="This skin tone already exists")