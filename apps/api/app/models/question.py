"""Question model."""

from sqlalchemy import Column, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    number = Column(String, nullable=False)
    text = Column(String, nullable=False)
    answer_type = Column(String, default="short")
    keywords = Column(JSON, default=list)
    model_answer = Column(String, nullable=True)
    marks = Column(Integer, default=5)

    exam = relationship("Exam", backref="questions")

