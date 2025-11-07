"""Processing routes for OCR and scoring."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.celery_app import celery_app
from app.core.database import async_session_factory
from app.repositories.submission import SubmissionRepository


router = APIRouter()


@router.post("/start/{submission_id}", summary="Start processing for a submission")
async def start_processing(submission_id: int, current_user: dict = Depends(get_current_user)) -> dict:
    async with async_session_factory() as session:
        repo = SubmissionRepository(session)
        submission = await repo.get(submission_id)
        if submission is None:
            raise HTTPException(status_code=404, detail="Submission not found")
    question_meta = {"keywords": ["innovation", "analysis"], "marks": 10, "answer_type": "long"}
    task = celery_app.send_task("app.tasks.pipeline.evaluate", args=[submission.id, question_meta])
    return {"submission_id": submission_id, "task_id": task.id, "status": "queued"}

