"""Evaluation model."""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    score_breakdown = Column(JSON, default=dict)
    final_score = Column(Float, default=0.0)
    confidence = Column(Float, default=0.0)
    feedback = Column(String, nullable=True)
    # ML evaluation fields
    student_answer = Column(Text, nullable=True)
    reference_answer = Column(Text, nullable=True)
    similarity = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    submission = relationship("Submission", back_populates="evaluation")



