"""Submissions listing endpoint."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.core.database import async_session_factory
from app.models import Submission


router = APIRouter()


@router.get("/submissions", summary="Get all submissions for current user")
async def list_submissions(current_user: dict = Depends(get_current_user)) -> dict:
    """Get all submissions for the current user."""
    try:
        async with async_session_factory() as session:
            user_id = int(current_user["id"])
            query = select(Submission).where(Submission.user_id == user_id).order_by(Submission.created_at.desc())
            result = await session.execute(query)
            submissions = result.scalars().all()
            
            # Process submissions outside of the session
            submission_list = []
            for sub in submissions:
                try:
                    submission_dict = {
                        "id": sub.id,
                        "exam_id": sub.exam_id,
                        "status": sub.status,
                        "storage_path": sub.storage_path,
                        "created_at": sub.created_at.isoformat() if sub.created_at else None,
                        "has_evaluation": sub.evaluation is not None if hasattr(sub, 'evaluation') else False,
                        "score": sub.evaluation.final_score if hasattr(sub, 'evaluation') and sub.evaluation else None,
                        "confidence": sub.evaluation.confidence if hasattr(sub, 'evaluation') and sub.evaluation else None,
                    }
                    submission_list.append(submission_dict)
                except Exception:
                    continue
            
            return {
                "submissions": submission_list,
                "total": len(submission_list)
            }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"submissions": [], "total": 0}

