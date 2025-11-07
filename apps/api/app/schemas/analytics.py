"""Analytics schemas."""

from datetime import datetime

from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    average_score: float
    confidence_distribution: dict[str, float]
    missed_keywords: dict[str, int]
    status_breakdown: dict[str, int]
    updated_at: datetime

