"""Upload routes."""

import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.auth.dependencies import get_current_user
from app.core.database import async_session_factory
from app.models import Submission
from app.repositories.submission import SubmissionRepository
from app.utils.storage import save_locally


router = APIRouter()


@router.post("/", summary="Upload an answer sheet")
async def upload_answer_sheet(
    exam_id: int = Form(...),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
) -> dict:
    try:
        # Get the base directory (apps/api)
        base_dir = Path(__file__).parent.parent.parent.parent
        storage_dir = base_dir / "storage"
        
        # Ensure storage directory exists
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        filename = f"{uuid.uuid4()}_{file.filename or 'upload'}"
        storage_path = storage_dir / filename
        
        # Read file content
        file_content = await file.read()
        
        if not file_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is empty"
            )
        
        # Save file
        save_locally(storage_path, file_content)
        
        # Store relative path in database
        relative_path = f"storage/{filename}"
        
        async with async_session_factory() as session:
            repo = SubmissionRepository(session)
            submission = Submission(
                user_id=int(current_user["id"]), 
                exam_id=exam_id, 
                storage_path=relative_path
            )
            submission = await repo.create(submission)

        return {
            "submission_id": submission.id, 
            "status": submission.status, 
            "storage_path": submission.storage_path
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

