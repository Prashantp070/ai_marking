"""Optical character recognition service leveraging TrOCR models."""

from __future__ import annotations

import functools
import logging
from typing import Any

try:
    from langdetect import detect
except ImportError:  # pragma: no cover
    detect = lambda text: "en"  # type: ignore

try:
    from transformers import TrOCRProcessor, VisionEncoderDecoderModel
    import torch
    from PIL import Image
except ImportError:  # pragma: no cover
    TrOCRProcessor = VisionEncoderDecoderModel = Image = torch = None  # type: ignore

from app.core.config import settings

logger = logging.getLogger(__name__)


class OCRService:
    def __init__(self) -> None:
        self.en_model_name = settings.OCR_MODEL_EN
        self.hi_model_name = settings.OCR_MODEL_HI

    @functools.lru_cache(maxsize=2)
    def _load_model(self, model_name: str) -> tuple[Any, Any] | None:
        if TrOCRProcessor is None or VisionEncoderDecoderModel is None:  # pragma: no cover
            logger.warning("Transformers not installed; OCR unavailable")
            return None
        processor = TrOCRProcessor.from_pretrained(model_name)
        model = VisionEncoderDecoderModel.from_pretrained(model_name)
        model.eval()
        return processor, model

    def _infer_language(self, image_text_hint: str | None = None) -> str:
        if image_text_hint:
            try:
                return detect(image_text_hint)
            except Exception:  # pragma: no cover - best effort
                return "en"
        return "en"

    def _detect_language(self, text: str, fallback: str) -> str:
        if not text:
            return fallback
        try:
            return detect(text)
        except Exception:  # pragma: no cover
            return fallback

    def _run_tesseract(self, image_path: str) -> tuple[str, float]:
        try:
            import pytesseract
            from PIL import Image

            text = pytesseract.image_to_string(Image.open(image_path), lang="eng+hin")
            return text.strip(), 0.6
        except Exception as exc:  # pragma: no cover
            logger.error("Tesseract fallback failed: %s", exc)
            return "", 0.0

    def run(self, image_path: str, language_hint: str | None = None) -> dict[str, Any]:
        language = language_hint if language_hint not in {None, "auto"} else None

        target_language = language or self._infer_language(None)
        model_name = self.hi_model_name if target_language.startswith("hi") else self.en_model_name
        model_bundle = self._load_model(model_name)
        if model_bundle is None:
            text, confidence = self._run_tesseract(image_path)
            detected_language = self._detect_language(text, target_language)
            return {"text": text, "confidence": confidence, "language": detected_language, "engine": "tesseract"}

        processor, model = model_bundle
        assert processor is not None and model is not None

        if Image is None or torch is None:  # pragma: no cover
            text, confidence = self._run_tesseract(image_path)
            detected_language = self._detect_language(text, target_language)
            return {"text": text, "confidence": confidence, "language": detected_language, "engine": "tesseract"}

        image = Image.open(image_path).convert("RGB")
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        with torch.no_grad():  # type: ignore[attr-defined]
            generated_ids = model.generate(pixel_values)
        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        detected_language = self._detect_language(text, target_language)
        confidence = 0.85 if detected_language.startswith("en") else 0.8
        return {"text": text.strip(), "confidence": confidence, "language": detected_language, "engine": "trocr"}

