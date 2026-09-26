from typing import List

from .detector import Detection


def filter_detections(
    detections: List[Detection],
    confidence_threshold: float = 0.50,
) -> List[Detection]:
    """Keep only detections meeting the confidence threshold."""
    return [
        detection
        for detection in detections
        if detection.confidence >= confidence_threshold
    ]
