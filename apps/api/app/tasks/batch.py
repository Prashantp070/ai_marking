"""Batch processing tasks."""

import logging

from app.celery_app import celery_app
from app.core.database import get_sync_session
from app.models import Job

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.batch.process")
def process_batch_job(job_id: str, files: list[str]) -> dict:
    logger.info("Processing batch job %s with %d files", job_id, len(files))
    with get_sync_session() as session:
        job: Job | None = session.query(Job).filter(Job.job_id == job_id).first()
        if job is None:
            logger.error("Job %s not found", job_id)
            return {"job_id": job_id, "processed": 0, "status": "missing"}

        total_files = max(len(files), 1)
        job.status = "processing"
        job.progress = 0.0
        session.commit()

        processed_files: list[dict] = []
        for index, file_path in enumerate(files, start=1):
            # TODO: enqueue individual OCR/scoring tasks per file_path
            processed_files.append({"file": file_path, "status": "processed"})
            job.progress = round(index / total_files, 2)
            session.commit()

        job.status = "completed"
        job.progress = 1.0
        job.result = {"processed_files": processed_files}
        session.commit()

        return {"job_id": job_id, "processed": len(processed_files), "status": job.status, "progress": job.progress}

