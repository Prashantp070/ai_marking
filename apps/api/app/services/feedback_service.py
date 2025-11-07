"""Feedback service handling teacher corrections and retraining stub."""

import logging

from app.models import Feedback
from app.repositories.feedback import FeedbackRepository

logger = logging.getLogger(__name__)


class FeedbackService:
    def __init__(self, repo: FeedbackRepository) -> None:
        self.repo = repo

    async def submit_feedback(self, *, evaluation_id: int, teacher_id: int, comments: str | None, suggested_score: float | None) -> Feedback:
        feedback = Feedback(
            evaluation_id=evaluation_id,
            teacher_id=teacher_id,
            comments=comments,
            suggested_score=suggested_score,
        )
        return await self.repo.create(feedback)

    async def retrain_model(self) -> None:
        logger.info("Retraining model with accumulated feedback (stub)")

