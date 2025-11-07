"""Analytics computation service."""

from __future__ import annotations

import datetime as dt
import logging
from collections import Counter

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Evaluation, Submission
from app.repositories.analytics_cache import AnalyticsCacheRepository

logger = logging.getLogger(__name__)


class AnalyticsService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.cache_repo = AnalyticsCacheRepository(session)

    @staticmethod
    def _prepare_response(payload: dict) -> dict:
        data = dict(payload)
        updated_at = data.get("updated_at")
        if isinstance(updated_at, str):
            try:
                data["updated_at"] = dt.datetime.fromisoformat(updated_at)
            except ValueError:
                logger.debug("Unable to parse updated_at %s", updated_at)
        return data

    async def get_overview(self) -> dict:
        cache = await self.cache_repo.get("overview")
        if cache and cache.payload:
            return self._prepare_response(cache.payload)

        scores_stmt = select(func.avg(Evaluation.final_score))
        confidence_stmt = select(Evaluation.confidence)
        keyword_gap_stmt = select(Submission.status, func.count(Submission.id)).group_by(Submission.status)
        evaluation_stmt = select(Evaluation.score_breakdown)

        average_score = (await self.session.execute(scores_stmt)).scalar() or 0.0
        confidences = [row[0] for row in (await self.session.execute(confidence_stmt)).all()]
        confidence_distribution = {
            "low": sum(1 for c in confidences if c < 0.6),
            "medium": sum(1 for c in confidences if 0.6 <= c < 0.8),
            "high": sum(1 for c in confidences if c >= 0.8),
        }
        status_breakdown = {status: count for status, count in (await self.session.execute(keyword_gap_stmt)).all()}

        missed_counter: Counter[str] = Counter()
        evaluation_rows = await self.session.execute(evaluation_stmt)
        for (score_breakdown,) in evaluation_rows:
            if not score_breakdown:
                continue
            scoring = score_breakdown.get("scoring", {})
            missing_keywords = scoring.get("missing_keywords", [])
            for keyword in missing_keywords:
                missed_counter[keyword] += 1

        timestamp = dt.datetime.utcnow().isoformat()
        payload = {
            "average_score": average_score,
            "confidence_distribution": confidence_distribution,
            "missed_keywords": dict(missed_counter),
            "status_breakdown": status_breakdown,
            "updated_at": timestamp,
        }
        await self.cache_repo.upsert("overview", payload)
        return self._prepare_response(payload)

