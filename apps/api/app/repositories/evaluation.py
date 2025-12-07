"""Evaluation repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Evaluation
from app.repositories.base import BaseRepository


class EvaluationRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_submission(self, submission_id: int) -> Evaluation | None:
        result = await self.session.execute(select(Evaluation).where(Evaluation.submission_id == submission_id))
        return result.scalars().first()

    async def create(self, evaluation: Evaluation) -> Evaluation:
        self.session.add(evaluation)
        await self.session.commit()
        await self.session.refresh(evaluation)
        return evaluation




