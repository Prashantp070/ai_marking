"""Database models for the platform."""

from app.core.database import Base  # noqa: F401

from .analytics_cache import AnalyticsCache  # noqa: F401
from .evaluation import Evaluation  # noqa: F401
from .exam import Exam  # noqa: F401
from .feedback import Feedback  # noqa: F401
from .job import Job  # noqa: F401
from .question import Question  # noqa: F401
from .submission import Submission  # noqa: F401
from .user import User  # noqa: F401

