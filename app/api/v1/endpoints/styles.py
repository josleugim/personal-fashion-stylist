from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.style import StyleCreate, StyleUpdate, StyleResponse
from app import crud

router = APIRouter()

@router.get("/{style_id}", response_model=StyleResponse)
async def get_style(style_id: int, db: AsyncSession = Depends(get_db)):
    style = await crud.style.get_style(db, style_id)
    if not style:
        raise HTTPException(status_code=404, detail="Style not found")
    return style

@router.get("/", response_model=list[StyleResponse])
async def get_styles(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.style.get_styles(db, skip=skip, limit=limit)

@router.post("/", response_model=StyleResponse, status_code=201)
async def create_style(style: StyleCreate, db: AsyncSession = Depends(get_db)):
    return await crud.style.create_style(db, style)

@router.patch("/{style_id}", response_model=StyleResponse)
async def update_style(style_id: int, style: StyleUpdate, db: AsyncSession = Depends(get_db)):
    db_style = await crud.style.get_style(db, style_id)
    if not db_style:
        raise HTTPException(status_code=404, detail="Style not found")
    return await crud.style.update_style(db, db_style, style)