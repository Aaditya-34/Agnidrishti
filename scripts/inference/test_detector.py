from typing import List

import numpy as np

from .detector import Detection
from .detector import Detector


class TestDetector(Detector):
    """Deterministic detector used only for pipeline testing."""

    def detect(self, frame: np.ndarray) -> List[Detection]:
        height, width = frame.shape[:2]

        box_width = max(40, width // 5)
        box_height = max(40, height // 5)

        x1 = width // 3
        y1 = height // 3
        x2 = min(width - 1, x1 + box_width)
        y2 = min(height - 1, y1 + box_height)

        return [
            Detection(
                class_id=0,
                class_name="test",
                confidence=0.90,
                x1=float(x1),
                y1=float(y1),
                x2=float(x2),
                y2=float(y2),
            )
        ]
