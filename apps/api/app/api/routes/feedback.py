"""Feedback submission routes."""

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.core.database import async_session_factory
from app.repositories.feedback import FeedbackRepository
from app.schemas.feedback import FeedbackCreate
from app.services.feedback_service import FeedbackService


router = APIRouter()


@router.post("/", summary="Submit feedback for an evaluation")
async def submit_feedback(payload: FeedbackCreate, current_user: dict = Depends(get_current_user)) -> dict:
    async with async_session_factory() as session:
        repo = FeedbackRepository(session)
        service = FeedbackService(repo)
        feedback = await service.submit_feedback(
            evaluation_id=payload.evaluation_id,
            teacher_id=int(current_user["id"]),
            comments=payload.comments,
            suggested_score=payload.suggested_score,
        )
    return {"feedback_id": feedback.id, "status": "received"}



