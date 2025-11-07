"""Teacher feedback model."""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comments = Column(String, nullable=True)
    suggested_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

