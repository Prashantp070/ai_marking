"""Submission model."""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    storage_path = Column(String, nullable=False)
    status = Column(String, default="uploaded")
    language = Column(String, default="en")
    ocr_confidence = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", backref="submissions")
    exam = relationship("Exam", backref="submissions")
    evaluation = relationship("Evaluation", back_populates="submission", uselist=False)

