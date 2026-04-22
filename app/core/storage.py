from google.cloud import storage
from app.core.config import settings
from PIL import Image

import uuid
import io

def upload_body_type_image(file_bytes: bytes, filename: str) -> dict:
    client = storage.Client.from_service_account_json(settings.GCS_CREDENTIALS_PATH)
    bucket = client.get_bucket(settings.GCS_BUCKET_NAME)

    unique_id = uuid.uuid4()
    safe_filename = filename.replace(" ", "_").lower()

    # ── 1. Prepare all image versions in memory FIRST ────────────
    images = {
        "original": file_bytes,
        "thumbnail": _generate_thumbnail(file_bytes, size=(300, 300))
    }

    # ── 2. Define GCS paths ──────────────────────────────────────
    paths = {
        "original": f"body_type/{unique_id}_{safe_filename}",
        "thumbnail": f"body_type/thumbnails/{unique_id}_{safe_filename}"
    }

    # ── 3. Upload each one separately ───────────────────────────
    urls = {}
    for key in images:
        urls[key] = _upload_blob(bucket, paths[key], images[key])

    return {
        "image_filename": f"{unique_id}_{safe_filename}",
        "image_url": urls["original"],
        "thumbnail_url": urls["thumbnail"]
    }


def upload_wardrobe_image(file_bytes: bytes, filename: str, profile_id: int) -> dict:
    client = storage.Client.from_service_account_json(settings.GCS_CREDENTIALS_PATH)
    bucket = client.bucket(settings.GCS_BUCKET_NAME)

    unique_id = uuid.uuid4()
    safe_filename = filename.replace(" ", "_").lower()

    # ── 1. Prepare all image versions in memory FIRST ────────────
    images = {
        "original": file_bytes,
        "thumbnail": _generate_thumbnail(file_bytes, size=(300, 300))
    }

    # ── 2. Define GCS paths ──────────────────────────────────────
    paths = {
        "original": f"wardrobe/{profile_id}/{unique_id}_{safe_filename}",
        "thumbnail": f"wardrobe/{profile_id}/thumbnails/{unique_id}_{safe_filename}"
    }

    # ── 3. Upload each one separately ───────────────────────────
    urls = {}
    for key in images:
        urls[key] = _upload_blob(bucket, paths[key], images[key])

    return {
        "image_filename": f"{unique_id}_{safe_filename}",
        "image_url": urls["original"],
        "thumbnail_url": urls["thumbnail"]
    }

def get_gcs_client():
    return storage.Client.from_service_account_json(
        settings.GCS_CREDENTIALS_PATH
    )

def _generate_thumbnail(file_bytes: bytes, size: tuple = (300, 300)) -> bytes:
    image = Image.open(io.BytesIO(file_bytes))

    # Convert RGBA or P (palette) to RGB so JPEG saving works
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # Resize maintaining aspect ratio — thumbnail() never stretches
    image.thumbnail(size)

    output = io.BytesIO()
    image.save(output, format="JPEG", quality=85, optimize=True)
    output.seek(0)
    return output.getvalue()

def _upload_blob(bucket, path: str, data: bytes) -> str:
    """Upload bytes to GCS and return the public URL."""
    blob = bucket.blob(path)
    blob.upload_from_file(
        io.BytesIO(data),          # ← use BytesIO stream, not raw bytes
        content_type="image/jpeg",
        rewind=True                # ← rewind stream before upload
    )
    blob.make_public()
    return blob.public_url