"""Upload file routes"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.core.security import FileValidator
from app.models import get_db, Upload as UploadModel
from app.services.file_processor import FileProcessor
from datetime import datetime

router = APIRouter(prefix="/api/uploads", tags=["uploads"])
file_processor = FileProcessor()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = get_db()):
    """Upload and process a file"""
    try:
        # Validate file
        if not FileValidator.is_allowed_file(file.filename):
            raise HTTPException(status_code=400, detail="File type not allowed")

        # Read file content
        content = await file.read()

        # Validate file size
        if not FileValidator.validate_file_size(len(content)):
            raise HTTPException(status_code=400, detail="File size exceeds limit")

        # Process file and extract text
        extracted_text = await file_processor.process_file(
            file.filename,
            content,
            file.content_type
        )

        # Save to database
        safe_filename = FileValidator.sanitize_filename(file.filename)
        upload = UploadModel(
            filename=safe_filename,
            original_filename=file.filename,
            file_type=file.content_type,
            file_path=f"uploads/{safe_filename}",
            content=extracted_text,
            file_size=len(content),
            upload_date=datetime.utcnow()
        )
        next(db).add(upload)
        next(db).commit()
        next(db).refresh(upload)

        logger.info(f"File uploaded successfully: {file.filename}")
        return {
            "success": True,
            "upload_id": upload.id,
            "filename": upload.original_filename,
            "file_size": upload.file_size,
            "content_preview": extracted_text[:500]
        }

    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_uploads(db: Session = get_db()):
    """List all uploaded files"""
    try:
        uploads = next(db).query(UploadModel).all()
        return {
            "success": True,
            "uploads": [
                {
                    "id": u.id,
                    "filename": u.original_filename,
                    "file_type": u.file_type,
                    "file_size": u.file_size,
                    "upload_date": u.upload_date
                }
                for u in uploads
            ]
        }
    except Exception as e:
        logger.error(f"Error listing uploads: {e}")
        raise HTTPException(status_code=500, detail=str(e))
