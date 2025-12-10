"""Batch job schemas."""

from datetime import datetime

from pydantic import BaseModel


class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: float
    result: dict | None = None
    created_at: datetime | None = None


class BatchRequest(BaseModel):
    exam_id: int
    files: list[str]





