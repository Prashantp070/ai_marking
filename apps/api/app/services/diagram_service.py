"""Diagram evaluation service."""

from __future__ import annotations

import logging
from typing import Any

try:
    import cv2  # type: ignore
    import numpy as np
except Exception:  # pragma: no cover
    cv2 = None  # type: ignore
    np = None  # type: ignore

logger = logging.getLogger(__name__)


class DiagramService:
    def __init__(self) -> None:
        self.edge_threshold = 80

    def analyze(self, image_path: str) -> dict[str, Any]:
        if cv2 is None or np is None:  # pragma: no cover
            logger.warning("OpenCV not available; returning default diagram analysis")
            return {"has_diagram": False, "edge_density": 0.0, "marks_multiplier": 0.5}
        try:
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            edges = cv2.Canny(image, self.edge_threshold, self.edge_threshold * 2)
            edge_density = float(np.sum(edges) / edges.size)
            has_diagram = edge_density > 0.05
            marks_multiplier = 1.0 if has_diagram else 0.5
            return {"has_diagram": has_diagram, "edge_density": edge_density, "marks_multiplier": marks_multiplier}
        except Exception as exc:  # pragma: no cover
            logger.error("Diagram analysis failed: %s", exc)
            return {"has_diagram": False, "edge_density": 0.0, "marks_multiplier": 0.5}

