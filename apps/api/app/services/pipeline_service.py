"""High-level orchestration utilities for evaluation pipeline."""

from __future__ import annotations

from typing import Any


def compute_final_confidence(*, ocr_conf: float, semantic_score: float, layout_conf: float) -> float:
    final_conf = ocr_conf * 0.4 + semantic_score * 0.5 + layout_conf * 0.1
    return round(final_conf, 4)


def flag_for_review(confidence: float, threshold: float = 0.7) -> bool:
    return confidence < threshold


def aggregate_scores(
    *,
    ocr_result: dict[str, Any],
    scoring_result: dict[str, Any],
    layout_result: dict[str, Any],
    diagram_result: dict[str, Any],
) -> dict[str, Any]:
    confidence = compute_final_confidence(
        ocr_conf=float(ocr_result.get("confidence", 0.0)),
        semantic_score=float(scoring_result.get("semantic_score", 0.0)),
        layout_conf=float(layout_result.get("confidence", 0.0)),
    )
    flagged = flag_for_review(confidence)
    raw_score = float(scoring_result.get("raw_score", scoring_result.get("final_marks", 0.0)))
    max_marks = float(scoring_result.get("max_marks", raw_score))
    diagram_multiplier = float(diagram_result.get("marks_multiplier", 1.0))
    adjusted_final = min(raw_score * diagram_multiplier, max_marks)

    scoring_details = {
        **scoring_result,
        "diagram_multiplier": diagram_multiplier,
        "final_marks": adjusted_final,
    }
    return {
        "final_marks": adjusted_final,
        "confidence": confidence,
        "flagged_for_review": flagged,
        "details": {
            "ocr": ocr_result,
            "scoring": scoring_details,
            "layout": layout_result,
            "diagram": diagram_result,
        },
    }

