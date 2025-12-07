"""Analytics cache model."""

from sqlalchemy import Column, DateTime, Integer, JSON, String
from sqlalchemy.sql import func

from app.core.database import Base


class AnalyticsCache(Base):
    __tablename__ = "analytics_cache"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    payload = Column(JSON, default=dict)
    computed_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())




