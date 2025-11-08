"""Result retrieval routes."""

from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.core.database import async_session_factory
from app.repositories.evaluation import EvaluationRepository


router = APIRouter()


@router.get("/{submission_id}", summary="Get evaluation results")
async def get_results(submission_id: int, current_user: dict = Depends(get_current_user)) -> dict:
    async with async_session_factory() as session:
        repo = EvaluationRepository(session)
        evaluation = await repo.get_by_submission(submission_id)
        if evaluation is None:
            raise HTTPException(status_code=404, detail="Results not ready")
        return {
            "status": "success",
            "submission_id": submission_id,
            "score": evaluation.final_score,
            "confidence": evaluation.confidence,
            "feedback": evaluation.feedback,
            "student_answer": evaluation.student_answer,
            "reference_answer": evaluation.reference_answer,
            "similarity": evaluation.similarity,
            "score_breakdown": evaluation.score_breakdown,
        }



