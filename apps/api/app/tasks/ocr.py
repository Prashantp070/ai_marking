"""Celery task for OCR pipeline."""

from app.celery_app import celery_app
from app.services.ocr_service import OCRService

ocr_service = OCRService()


@celery_app.task(name="app.tasks.ocr.run")
def ocr_pipeline(image_path: str, language_hint: str | None = None) -> dict:
    return ocr_service.run(image_path, language_hint)



