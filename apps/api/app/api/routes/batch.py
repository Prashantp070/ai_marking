"""Batch processing routes."""

from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.celery_app import celery_app
from app.core.database import async_session_factory
from app.repositories.job import JobRepository
from app.schemas.jobs import BatchRequest, JobStatus
from app.services.batch_service import BatchProcessingService


router = APIRouter()


@router.post("/", response_model=JobStatus, summary="Create a batch processing job")
async def create_batch_job(payload: BatchRequest, current_user: dict = Depends(get_current_user)) -> JobStatus:
    async with async_session_factory() as session:
        service = BatchProcessingService(JobRepository(session))
        job = await service.create_job("batch_upload", metadata={"exam_id": payload.exam_id, "user_id": current_user["id"]})

    celery_app.send_task("app.tasks.batch.process", args=[job.job_id, payload.files])
    return JobStatus(job_id=job.job_id, status=job.status, progress=job.progress, created_at=job.created_at)


@router.get("/{job_id}", response_model=JobStatus, summary="Get batch job status")
async def get_batch_job(job_id: str, current_user: dict = Depends(get_current_user)) -> JobStatus:
    async with async_session_factory() as session:
        repo = JobRepository(session)
        job = await repo.get_by_job_id(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return JobStatus(job_id=job.job_id, status=job.status, progress=job.progress, result=job.result, created_at=job.created_at)

