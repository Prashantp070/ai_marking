"""Celery task for scoring pipeline."""

from app.celery_app import celery_app
from app.services.scoring_service import ScoringService

scoring_service = ScoringService()


@celery_app.task(name="app.tasks.scoring.run")
def scoring_pipeline(answer: str, question_meta: dict) -> dict:
    return scoring_service.score(answer=answer, question_meta=question_meta)




