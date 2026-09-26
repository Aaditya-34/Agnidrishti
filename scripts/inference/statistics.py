from collections import defaultdict
from typing import Dict, List

from .detector import Detection


class ConfidenceStatistics:
    """Collect per-class detection confidence statistics."""

    def __init__(self):
        self._confidences = defaultdict(list)

    def update(self, detections: List[Detection]) -> None:
        for detection in detections:
            self._confidences[detection.class_name].append(
                detection.confidence
            )

    def summary(self) -> Dict[str, dict]:
        result = {}

        for class_name, confidences in sorted(self._confidences.items()):
            result[class_name] = {
                "detections": len(confidences),
                "average_confidence": round(
                    sum(confidences) / len(confidences),
                    4,
                ),
                "maximum_confidence": round(
                    max(confidences),
                    4,
                ),
                "minimum_confidence": round(
                    min(confidences),
                    4,
                ),
            }

        return result
