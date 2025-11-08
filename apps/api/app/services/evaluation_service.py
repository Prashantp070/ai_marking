"""ML-based evaluation service using sentence-transformers for semantic similarity."""

import functools
import logging
from typing import Any

try:
    from sentence_transformers import SentenceTransformer, util
    import numpy as np
except ImportError:
    SentenceTransformer = None
    util = None
    np = None

from app.core.config import settings

logger = logging.getLogger(__name__)


class EvaluationService:
    """Service for ML-based answer evaluation using semantic similarity."""

    def __init__(self) -> None:
        """Initialize the evaluation service and load the ML model."""
        self.model = self._load_model()
        if self.model is None:
            logger.warning("SentenceTransformer not available. ML evaluation will not work properly.")

    @functools.lru_cache(maxsize=1)
    def _load_model(self) -> Any | None:
        """Load the sentence transformer model once at startup."""
        if SentenceTransformer is None:
            logger.warning("SentenceTransformer not installed; ML evaluation unavailable")
            return None
        
        try:
            # Use paraphrase-MiniLM-L6-v2 for semantic similarity
            model_name = "paraphrase-MiniLM-L6-v2"
            logger.info(f"Loading ML model: {model_name}")
            model = SentenceTransformer(model_name)
            logger.info("ML model loaded successfully")
            return model
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")
            return None

    def evaluate_answer(self, student_text: str, reference_text: str) -> dict[str, Any]:
        """
        Evaluate student answer against reference answer using ML semantic similarity.
        
        Args:
            student_text: The student's answer text (from OCR)
            reference_text: The reference/model answer text
            
        Returns:
            Dictionary with score (0-10), confidence (0-1), and similarity (0-1)
        """
        if self.model is None or util is None:
            logger.warning("ML model not available, using fallback scoring")
            # Fallback to simple text similarity
            similarity = self._fallback_similarity(student_text, reference_text)
            score = self._similarity_to_score(similarity)
            confidence = similarity
            return {
                "score": score,
                "confidence": confidence,
                "similarity": similarity,
                "method": "fallback"
            }

        try:
            # Normalize texts
            student_text = student_text.strip()
            reference_text = reference_text.strip()
            
            if not student_text or not reference_text:
                return {
                    "score": 0.0,
                    "confidence": 0.0,
                    "similarity": 0.0,
                    "method": "ml"
                }

            # Generate embeddings
            embeddings = self.model.encode(
                [student_text, reference_text],
                convert_to_tensor=True,
                show_progress_bar=False
            )

            # Calculate cosine similarity
            similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
            
            # Normalize similarity to 0-1 range (cosine similarity is already -1 to 1, but typically 0-1)
            similarity = max(0.0, min(1.0, (similarity + 1) / 2))
            
            # Convert similarity to score (0-10)
            score = self._similarity_to_score(similarity)
            
            # Confidence is the normalized similarity
            confidence = similarity

            logger.debug(
                f"Evaluation: similarity={similarity:.3f}, score={score:.2f}, confidence={confidence:.3f}"
            )

            return {
                "score": round(score, 2),
                "confidence": round(confidence, 3),
                "similarity": round(similarity, 3),
                "method": "ml"
            }

        except Exception as e:
            logger.error(f"Error in ML evaluation: {e}", exc_info=True)
            # Fallback to simple similarity
            similarity = self._fallback_similarity(student_text, reference_text)
            score = self._similarity_to_score(similarity)
            return {
                "score": score,
                "confidence": similarity,
                "similarity": similarity,
                "method": "fallback_error"
            }

    def _similarity_to_score(self, similarity: float) -> float:
        """
        Convert similarity (0-1) to score (0-10) based on thresholds.
        
        - similarity < 0.4 → score = 2
        - 0.4 <= similarity < 0.7 → score = 5
        - similarity >= 0.7 → score = 8-10 (linear mapping)
        """
        if similarity < 0.4:
            return 2.0
        elif similarity < 0.7:
            # Linear mapping from 0.4-0.7 to 2-8
            return 2.0 + (similarity - 0.4) * (8.0 - 2.0) / (0.7 - 0.4)
        else:
            # Linear mapping from 0.7-1.0 to 8-10
            return 8.0 + (similarity - 0.7) * (10.0 - 8.0) / (1.0 - 0.7)

    def _fallback_similarity(self, text1: str, text2: str) -> float:
        """Fallback similarity calculation when ML model is unavailable."""
        if not text1 or not text2:
            return 0.0
        
        # Simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)


# Global instance (singleton pattern)
_evaluation_service: EvaluationService | None = None


def get_evaluation_service() -> EvaluationService:
    """Get or create the global evaluation service instance."""
    global _evaluation_service
    if _evaluation_service is None:
        _evaluation_service = EvaluationService()
    return _evaluation_service

