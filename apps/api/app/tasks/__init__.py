"""Celery task modules."""

from .ocr import ocr_pipeline  # noqa: F401
from .scoring import scoring_pipeline  # noqa: F401
from .batch import process_batch_job  # noqa: F401
from .pipeline import evaluate_submission  # noqa: F401

