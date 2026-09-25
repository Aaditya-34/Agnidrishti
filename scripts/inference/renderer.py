from typing import List

import cv2
import numpy as np

from .tracker import Track


def render_tracks(
    frame: np.ndarray,
    tracks: List[Track],
) -> np.ndarray:
    """Draw tracked detections on a video frame."""

    output = frame.copy()

    for track in tracks:
        detection = track.detection

        x1 = int(round(detection.x1))
        y1 = int(round(detection.y1))
        x2 = int(round(detection.x2))
        y2 = int(round(detection.y2))

        label = (
            f"{detection.class_name} "
            f"{detection.confidence:.2f} "
            f"ID:{track.track_id}"
        )

        cv2.rectangle(
            output,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2,
        )

        cv2.putText(
            output,
            label,
            (x1, max(20, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

    return output
