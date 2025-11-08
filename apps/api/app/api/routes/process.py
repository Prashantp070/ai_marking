"""Processing routes for OCR and ML-based evaluation."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.celery_app import celery_app
from app.core.database import async_session_factory
from app.models import Question
from app.repositories.submission import SubmissionRepository


router = APIRouter()


@router.post("/start/{submission_id}", summary="Start ML-based evaluation for a submission")
async def start_processing(submission_id: int, current_user: dict = Depends(get_current_user)) -> dict:
    async with async_session_factory() as session:
        repo = SubmissionRepository(session)
        submission = await repo.get(submission_id)
        if submission is None:
            raise HTTPException(status_code=404, detail="Submission not found")
        
        # Get question for this exam (using first question as default, or get from exam_id)
        # For now, we'll use a default question or get from exam
        question_meta = {
            "keywords": [],
            "marks": 10,
            "answer_type": "long",
            "model_answer": "Photosynthesis is the process by which plants convert sunlight, water, and carbon dioxide into glucose and oxygen using chlorophyll in their leaves."
        }
        
        # Try to get question from database if exam_id is available
        if hasattr(submission, 'exam_id') and submission.exam_id:
            result = await session.execute(
                select(Question).where(Question.exam_id == submission.exam_id).limit(1)
            )
            question = result.scalar_one_or_none()
            if question:
                question_meta = {
                    "keywords": question.keywords or [],
                    "marks": question.marks or 10,
                    "answer_type": question.answer_type or "long",
                    "model_answer": question.model_answer or question_meta["model_answer"]
                }
    
    task = celery_app.send_task("app.tasks.pipeline.evaluate", args=[submission.id, question_meta])
    return {"submission_id": submission_id, "task_id": task.id, "status": "queued"}

