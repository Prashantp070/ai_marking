"""Feedback schemas."""

from datetime import datetime

from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    evaluation_id: int
    comments: str | None = None
    suggested_score: float | None = None


class FeedbackRead(FeedbackCreate):
    id: int
    teacher_id: int
    created_at: datetime

    class Config:
        from_attributes = True

