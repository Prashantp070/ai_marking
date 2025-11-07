"""Scoring service combining keyword and semantic similarity."""

from __future__ import annotations

import functools
import logging
from typing import Any

from rapidfuzz import fuzz

try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:  # pragma: no cover
    SentenceTransformer = None  # type: ignore
    util = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from deep_translator import GoogleTranslator
except Exception:  # pragma: no cover
    GoogleTranslator = None  # type: ignore

from app.core.config import settings
from app.utils.text import normalize_text

logger = logging.getLogger(__name__)


class ScoringService:
    def __init__(self) -> None:
        self.kw_weight = settings.KW_WEIGHT
        self.sem_weight = settings.SEM_WEIGHT

    @functools.lru_cache(maxsize=1)
    def _load_model(self) -> Any | None:
        if SentenceTransformer is None:
            logger.warning("SentenceTransformer not installed; semantic scores will be approximate")
            return None
        return SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)

    def _translate(self, text: str) -> str:
        if GoogleTranslator is None:
            return text
        try:
            translator = GoogleTranslator(source="auto", target="en")
            return translator.translate(text)
        except Exception as exc:  # pragma: no cover
            logger.error("Translation failed: %s", exc)
            return text

    def _keyword_score(self, answer: str, keywords: list[str]) -> tuple[float, list[str], list[str]]:
        if not keywords:
            return 0.0, [], []

        normalized_answer = normalize_text(answer)
        total_score = 0.0
        matched: list[str] = []
        missed: list[str] = []

        for keyword in keywords:
            normalized_kw = normalize_text(keyword)
            score = fuzz.partial_ratio(normalized_answer, normalized_kw) / 100
            total_score += score
            if score >= 0.7:
                matched.append(keyword)
            else:
                missed.append(keyword)

        average = total_score / len(keywords)
        return average, matched, missed

    def _semantic_score(self, answer: str, model_answer: str) -> float:
        model = self._load_model()
        if model is None or util is None:
            return fuzz.ratio(answer.lower(), model_answer.lower()) / 100
        embeddings = model.encode([answer, model_answer], convert_to_tensor=True)
        score = util.cos_sim(embeddings[0], embeddings[1]).item()
        return (score + 1) / 2  # normalize to 0-1

    def score(self, *, answer: str, question_meta: dict[str, Any]) -> dict[str, Any]:
        keywords = question_meta.get("keywords", [])
        model_answer = question_meta.get("model_answer", "")
        marks = question_meta.get("marks", 5)
        answer_type = question_meta.get("answer_type", "short")
        language = question_meta.get("language", "en")

        processed_answer = answer
        processed_model_answer = model_answer
        if language.startswith("hi"):
            processed_answer = self._translate(answer)
            processed_model_answer = self._translate(model_answer)

        kw_score, matched_keywords, missing_keywords = self._keyword_score(processed_answer, keywords)
        sem_score = self._semantic_score(processed_answer, processed_model_answer)

        weight_adjustment = 1.0
        if answer_type == "long":
            weight_adjustment = 1.1
        elif answer_type == "very_long":
            weight_adjustment = 1.2

        raw_score = (self.kw_weight * kw_score + self.sem_weight * sem_score) * marks * weight_adjustment
        final_marks = min(raw_score, marks)
        return {
            "final_marks": final_marks,
            "raw_score": raw_score,
            "max_marks": marks,
            "keyword_score": kw_score,
            "semantic_score": sem_score,
            "answer_type": answer_type,
            "language": language,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
        }

