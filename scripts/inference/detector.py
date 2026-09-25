from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List

import numpy as np


@dataclass
class Detection:
    class_id: int
    class_name: str
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float


class Detector(ABC):
    """Model-agnostic interface for object detectors."""

    @abstractmethod
    def detect(self, frame: np.ndarray) -> List[Detection]:
        """Run inference on one BGR video frame."""
        raise NotImplementedError
