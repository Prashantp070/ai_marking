"""Job repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Job
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_job_id(self, job_id: str) -> Job | None:
        result = await self.session.execute(select(Job).where(Job.job_id == job_id))
        return result.scalars().first()

    async def create(self, job: Job) -> Job:
        self.session.add(job)
        await self.session.commit()
        await self.session.refresh(job)
        return job

    async def update_progress(self, job: Job, status: str, progress: float, result: dict | None = None) -> Job:
        job.status = status
        job.progress = progress
        if result is not None:
            job.result = result
        await self.session.commit()
        await self.session.refresh(job)
        return job




