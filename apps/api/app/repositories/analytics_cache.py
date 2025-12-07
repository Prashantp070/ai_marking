"""Analytics cache repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AnalyticsCache
from app.repositories.base import BaseRepository


class AnalyticsCacheRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get(self, key: str) -> AnalyticsCache | None:
        result = await self.session.execute(select(AnalyticsCache).where(AnalyticsCache.key == key))
        return result.scalars().first()

    async def upsert(self, key: str, payload: dict) -> AnalyticsCache:
        cache = await self.get(key)
        if cache is None:
            cache = AnalyticsCache(key=key, payload=payload)
            self.session.add(cache)
        else:
            cache.payload = payload
        await self.session.commit()
        await self.session.refresh(cache)
        return cache




