"""Upload routes."""

import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, UploadFile

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
    filename = f"{uuid.uuid4()}_{file.filename}"
    storage_path = Path("storage") / filename
    save_locally(storage_path, await file.read())

    async with async_session_factory() as session:
        repo = SubmissionRepository(session)
        submission = Submission(user_id=int(current_user["id"]), exam_id=exam_id, storage_path=str(storage_path))
        submission = await repo.create(submission)

    return {"submission_id": submission.id, "status": submission.status, "storage_path": submission.storage_path}

