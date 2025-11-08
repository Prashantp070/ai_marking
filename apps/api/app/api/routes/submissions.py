"""Submissions listing endpoint."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.core.database import async_session_factory
from app.models import Submission


router = APIRouter()


@router.get("/", summary="Get all submissions for current user")
async def list_submissions(current_user: dict = Depends(get_current_user)) -> dict:
    """Get all submissions for the current user."""
    async with async_session_factory() as session:
        user_id = int(current_user["id"])
        result = await session.execute(
            select(Submission).where(Submission.user_id == user_id).order_by(Submission.created_at.desc())
        )
        submissions = result.scalars().all()
        
        return {
            "submissions": [
                {
                    "id": sub.id,
                    "exam_id": sub.exam_id,
                    "status": sub.status,
                    "created_at": sub.created_at.isoformat() if sub.created_at else None,
                    "has_evaluation": sub.evaluation is not None,
                    "score": sub.evaluation.final_score if sub.evaluation else None,
                    "confidence": sub.evaluation.confidence if sub.evaluation else None,
                }
                for sub in submissions
            ],
            "total": len(submissions)
        }

