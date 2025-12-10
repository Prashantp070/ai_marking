"""Feedback repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Feedback
from app.repositories.base import BaseRepository


class FeedbackRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, feedback: Feedback) -> Feedback:
        self.session.add(feedback)
        await self.session.commit()
        await self.session.refresh(feedback)
        return feedback

    async def list_for_evaluation(self, evaluation_id: int) -> list[Feedback]:
        result = await self.session.execute(select(Feedback).where(Feedback.evaluation_id == evaluation_id))
        return result.scalars().all()





