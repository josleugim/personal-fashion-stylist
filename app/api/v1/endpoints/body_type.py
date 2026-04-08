from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.storage import upload_body_type_image
from app.db.session import get_db
from app.schemas.body_type import BodyTypeCreate, BodyTypeUpdate, BodyTypeResponse
from app import crud

router = APIRouter()

@router.get("/", response_model=list[BodyTypeResponse])
async def get_all_body_types(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.body_type.get_body_types(db, skip=skip, limit=limit)

@router.post("/", response_model=BodyTypeResponse, status_code=201)
async def create_body_type(body_type: BodyTypeCreate, db: AsyncSession = Depends(get_db)):
    file_bytes = await body_type.file.read()

    if len(file_bytes) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="Image must be under 10MB.")

    try:
        image_data = upload_body_type_image(
            file_bytes,
            filename=body_type.file.filename,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"GCS upload failed: {str(e)}")

    return await crud.body_type.create_body_type(db, body_type, image_data)