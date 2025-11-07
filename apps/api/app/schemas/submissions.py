"""Submission related schemas."""

from datetime import datetime

from pydantic import BaseModel


class SubmissionBase(BaseModel):
    exam_id: int
    language: str | None = "en"


class SubmissionCreate(SubmissionBase):
    file_path: str


class SubmissionRead(SubmissionBase):
    id: int
    status: str
    storage_path: str
    created_at: datetime

    class Config:
        from_attributes = True

