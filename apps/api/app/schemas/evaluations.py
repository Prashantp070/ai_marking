"""Evaluation schemas."""

from datetime import datetime

from pydantic import BaseModel


class EvaluationRead(BaseModel):
    id: int
    submission_id: int
    final_score: float
    confidence: float
    feedback: str | None
    score_breakdown: dict
    created_at: datetime

    class Config:
        from_attributes = True

