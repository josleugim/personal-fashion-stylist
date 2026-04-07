from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.storage import upload_wardrobe_image
from app.core.claude import analyze_wardrobe_item
from app.crud import wardrobe as crud_wardrobe
from app.schemas.wardrobe import WardrobeResponse
from typing import Optional
import base64

router = APIRouter()

@router.post("/", response_model=WardrobeResponse)
async def upload_wardrobe_item(
    profile_id: int       = Form(...),
    name:    Optional[str] = Form(None),
    brand:   Optional[str] = Form(None),
    notes:   Optional[str] = Form(None),
    file:    UploadFile = File(...),
    db:      AsyncSession = Depends(get_db)
):
    # ── 1. Read image bytes ──────────────────────────────────────
    file_bytes = await file.read()

    if len(file_bytes) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="Image must be under 10MB.")

    # ── 2. Upload to Google Cloud Storage ───────────────────────
    try:
        image_data = upload_wardrobe_image(
            file_bytes=file_bytes,
            filename=file.filename,
            profile_id=profile_id
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"GCS upload failed: {str(e)}")

    # ── 3. Call Claude to auto-tag the item ─────────────────────
    try:
        image_base64 = base64.b64encode(file_bytes).decode("utf-8")
        ai_data = await analyze_wardrobe_item(image_base64)
    except Exception as e:
        # Don't block the upload if AI fails — save with empty tags
        ai_data = {}

    # ── 4. Save everything to the database ──────────────────────
    item = await crud_wardrobe.create(
        db=db,
        profile_id=profile_id,
        image_data=image_data,
        ai_data=ai_data,
        user_data={"name": name, "brand": brand, "notes": notes}
    )

    return item


@router.get("/{profile_id}", response_model=list[WardrobeResponse])
async def get_wardrobe(profile_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_wardrobe.get_by_user(db, profile_id)


@router.delete("/{item_id}")
async def delete_wardrobe_item(item_id: int, profile_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud_wardrobe.delete(db, item_id, profile_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found.")
    return {"success": True, "message": "Item removed from wardrobe."}