"""Background job model for batch processing."""

from sqlalchemy import Column, DateTime, Float, Integer, JSON, String
from sqlalchemy.sql import func

from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, nullable=False, index=True)
    job_type = Column(String, nullable=False)
    status = Column(String, default="pending")
    progress = Column(Float, default=0.0)
    job_metadata = Column(JSON, default=dict)  # renamed from `metadata`
    result = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
