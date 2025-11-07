"""Celery pipeline task combining OCR, layout detection, scoring, and persistence."""

from app.celery_app import celery_app
from app.core.database import get_sync_session
from app.models import Evaluation, Submission
from app.services.diagram_service import DiagramService
from app.services.layout_service import LayoutService
from app.services.ocr_service import OCRService
from app.services.pipeline_service import aggregate_scores
from app.services.scoring_service import ScoringService

ocr_service = OCRService()
layout_service = LayoutService()
diagram_service = DiagramService()
scoring_service = ScoringService()


@celery_app.task(name="app.tasks.pipeline.evaluate")
def evaluate_submission(submission_id: int, question_meta: dict) -> dict:
    with get_sync_session() as session:
        submission: Submission | None = session.get(Submission, submission_id)
        if submission is None:
            return {"status": "not_found"}

        ocr_result = ocr_service.run(submission.storage_path, submission.language)
        layout_result = layout_service.detect(submission.storage_path)
        diagram_result = diagram_service.analyze(submission.storage_path)

        scoring_result = scoring_service.score(answer=ocr_result.get("text", ""), question_meta=question_meta)

        aggregated = aggregate_scores(
            ocr_result=ocr_result,
            scoring_result=scoring_result,
            layout_result=layout_result,
            diagram_result=diagram_result,
        )

        evaluation = session.query(Evaluation).filter_by(submission_id=submission_id).first()
        if evaluation is None:
            evaluation = Evaluation(submission_id=submission_id)
            session.add(evaluation)

        evaluation.final_score = aggregated["final_marks"]
        evaluation.confidence = aggregated["confidence"]
        evaluation.score_breakdown = aggregated["details"]
        evaluation.feedback = "Flagged for review" if aggregated["flagged_for_review"] else "Auto-graded"

        submission.ocr_confidence = ocr_result.get("confidence")
        submission.language = ocr_result.get("language", submission.language)
        submission.status = "flagged" if aggregated["flagged_for_review"] else "graded"

        session.commit()

        return {"status": submission.status, "evaluation_id": evaluation.id, "confidence": evaluation.confidence}

