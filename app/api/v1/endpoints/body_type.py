from typing import Optional
from fastapi import Depends, HTTPException, APIRouter, Form, File, UploadFile
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
async def create_body_type(
    name: str = Form(...),
    description: str = Form(...),
    is_active: bool = Form(True),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    file_bytes = await file.read()

    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image must be under 10MB.")

    try:
        image_data = upload_body_type_image(file_bytes, filename=file.filename)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"GCS upload failed: {str(e)}")

    body_type = BodyTypeCreate(name=name, description=description, is_active=is_active)
    return await crud.body_type.create_body_type(db, body_type, image_data)

@router.put("/{body_type_id}", response_model=BodyTypeResponse, status_code=200)
async def update_body_type(
    body_type_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):
    image_data = None
    if file is not None:
        file_bytes = await file.read()

        if len(file_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image must be under 10MB.")

        try:
            image_data = upload_body_type_image(file_bytes, filename=file.filename)
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"GCS upload failed: {str(e)}")

    body_type = BodyTypeUpdate(name=name, description=description, is_active=is_active)
    result = await crud.body_type.put_body_type(db, body_type_id, body_type, image_data)
    if result is None:
        raise HTTPException(status_code=404, detail="Body type not found")
    return result