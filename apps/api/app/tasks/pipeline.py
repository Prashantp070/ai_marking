"""Celery pipeline task combining OCR, layout detection, ML evaluation, and persistence."""

from app.celery_app import celery_app
from app.core.database import get_sync_session
from app.models import Evaluation, Submission
from app.services.diagram_service import DiagramService
from app.services.evaluation_service import get_evaluation_service
from app.services.layout_service import LayoutService
from app.services.ocr_service import OCRService
from app.services.pipeline_service import aggregate_scores
from app.services.scoring_service import ScoringService

ocr_service = OCRService()
layout_service = LayoutService()
diagram_service = DiagramService()
scoring_service = ScoringService()
evaluation_service = get_evaluation_service()


@celery_app.task(name="app.tasks.pipeline.evaluate")
def evaluate_submission(submission_id: int, question_meta: dict) -> dict:
    with get_sync_session() as session:
        submission: Submission | None = session.get(Submission, submission_id)
        if submission is None:
            return {"status": "not_found"}

        # Run OCR to get student answer text
        ocr_result = ocr_service.run(submission.storage_path, submission.language)
        student_text = ocr_result.get("text", "")
        
        # Get reference answer from question metadata
        reference_text = question_meta.get("model_answer", "")
        
        # Run ML-based evaluation
        ml_evaluation = evaluation_service.evaluate_answer(student_text, reference_text)
        
        # Also run traditional scoring for compatibility
        layout_result = layout_service.detect(submission.storage_path)
        diagram_result = diagram_service.analyze(submission.storage_path)
        scoring_result = scoring_service.score(answer=student_text, question_meta=question_meta)

        aggregated = aggregate_scores(
            ocr_result=ocr_result,
            scoring_result=scoring_result,
            layout_result=layout_result,
            diagram_result=diagram_result,
        )

        # Use ML evaluation score and confidence as primary
        evaluation = session.query(Evaluation).filter_by(submission_id=submission_id).first()
        if evaluation is None:
            evaluation = Evaluation(submission_id=submission_id)
            session.add(evaluation)

        # Store ML evaluation results
        evaluation.final_score = ml_evaluation["score"]  # ML score (0-10)
        evaluation.confidence = ml_evaluation["confidence"]  # ML confidence
        evaluation.similarity = ml_evaluation["similarity"]  # ML similarity
        evaluation.student_answer = student_text
        evaluation.reference_answer = reference_text
        
        # Store breakdown with ML details
        evaluation.score_breakdown = {
            **aggregated["details"],
            "ml_evaluation": {
                "score": ml_evaluation["score"],
                "confidence": ml_evaluation["confidence"],
                "similarity": ml_evaluation["similarity"],
                "method": ml_evaluation["method"]
            }
        }
        
        # Flag for review if confidence is low
        if ml_evaluation["confidence"] < 0.5:
            evaluation.feedback = "Low AI confidence - Teacher review needed"
            submission.status = "flagged"
        else:
            evaluation.feedback = "Auto-graded with ML"
            submission.status = "graded"

        submission.ocr_confidence = ocr_result.get("confidence")
        submission.language = ocr_result.get("language", submission.language)

        session.commit()

        return {
            "status": submission.status,
            "evaluation_id": evaluation.id,
            "score": ml_evaluation["score"],
            "confidence": ml_evaluation["confidence"],
            "student_answer": student_text,
            "reference_answer": reference_text
        }

