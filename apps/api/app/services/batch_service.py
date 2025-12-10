"""Batch processing service for bulk uploads."""

import uuid

from app.models import Job
from app.repositories.job import JobRepository


class BatchProcessingService:
    def __init__(self, job_repo: JobRepository) -> None:
        self.job_repo = job_repo

    async def create_job(self, job_type: str, metadata: dict | None = None) -> Job:
        job = Job(job_id=str(uuid.uuid4()), job_type=job_type, metadata=metadata or {})
        return await self.job_repo.create(job)





