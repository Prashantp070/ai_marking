"""Celery application factory."""

from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "ai_handwritten",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_routes={
        "app.tasks.ocr.*": {"queue": "ocr"},
        "app.tasks.scoring.*": {"queue": "scoring"},
        "app.tasks.batch.*": {"queue": "batch"},
        "app.tasks.pipeline.*": {"queue": "pipeline"},
    },
    task_default_queue="default",
)


@celery_app.task(name="app.celery.health_check")
def health_check() -> str:
    return "healthy"

