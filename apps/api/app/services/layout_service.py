"""Layout detection using YOLOv8 stubs."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class LayoutService:
    def __init__(self) -> None:
        try:
            from ultralytics import YOLO  # type: ignore

            self.model = YOLO("yolov8n.pt")
        except Exception as exc:  # pragma: no cover - optional dependency
            logger.warning("YOLOv8 not available: %s", exc)
            self.model = None

    def detect(self, image_path: str) -> dict[str, Any]:
        if self.model is None:
            logger.debug("Returning stub layout detection result")
            return {"boxes": [], "confidence": 0.5, "question_segments": []}

        results = self.model(image_path)
        boxes = []
        for result in results:
            for box in result.boxes:
                boxes.append(
                    {
                        "bbox": box.xyxy[0].tolist(),
                        "confidence": float(box.conf[0]),
                        "label": result.names[int(box.cls[0])],
                    }
                )
        confidence = sum(item["confidence"] for item in boxes) / len(boxes) if boxes else 0.5
        question_segments = [
            {
                "question": f"Q{index + 1}",
                "bbox": entry["bbox"],
                "label": entry["label"],
                "confidence": entry["confidence"],
            }
            for index, entry in enumerate(boxes)
        ]
        return {"boxes": boxes, "confidence": confidence, "question_segments": question_segments}

