"""Submission repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Submission
from app.repositories.base import BaseRepository


class SubmissionRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get(self, submission_id: int) -> Submission | None:
        result = await self.session.execute(select(Submission).where(Submission.id == submission_id))
        return result.scalars().first()

    async def create(self, submission: Submission) -> Submission:
        self.session.add(submission)
        await self.session.commit()
        await self.session.refresh(submission)
        return submission





