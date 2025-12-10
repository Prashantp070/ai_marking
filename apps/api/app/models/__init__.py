"""
Central export for all SQLAlchemy models.

Iss file ka use karke hum likh sakte hain:
    from app.models import User, Exam, Question, Submission, Evaluation, Feedback, Job

Aur saare models ek hi jagah se mil jayenge.
"""
from app.core.database import Base

# User
try:
    from .user import User  # type: ignore
except Exception:  # pragma: no cover
    User = None  # type: ignore

# Submission
try:
    from .submission import Submission  # type: ignore
except Exception:  # pragma: no cover
    Submission = None  # type: ignore

# Evaluation
try:
    from .evaluation import Evaluation  # type: ignore
except Exception:  # pragma: no cover
    Evaluation = None  # type: ignore

# Exam
try:
    from .exam import Exam  # type: ignore
except Exception:  # pragma: no cover
    Exam = None  # type: ignore

# Question
try:
    from .question import Question  # type: ignore
except Exception:  # pragma: no cover
    Question = None  # type: ignore

# Feedback
try:
    from .feedback import Feedback  # type: ignore
except Exception:  # pragma: no cover
    Feedback = None  # type: ignore

# Job
try:
    from .job import Job  # type: ignore
except Exception:  # pragma: no cover
    Job = None  # type: ignore

# Analytics cache
try:
    from .analytics_cache import AnalyticsCache  # type: ignore
except Exception:  # pragma: no cover
    AnalyticsCache = None  # type: ignore
