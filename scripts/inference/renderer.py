from typing import List

import cv2
import numpy as np

from .tracker import Track


def render_tracks(
    frame: np.ndarray,
    tracks: List[Track],
) -> np.ndarray:
    """Draw tracked fire and smoke detections with class-specific colors."""

    output = frame.copy()

    for track in tracks:
        detection = track.detection

        x1 = int(round(detection.x1))
        y1 = int(round(detection.y1))
        x2 = int(round(detection.x2))
        y2 = int(round(detection.y2))

        class_name = detection.class_name.lower()

        # OpenCV uses BGR color order.
        if class_name == "fire":
            color = (0, 0, 255)       # Red
        elif class_name == "smoke":
            color = (255, 0, 0)       # Blue
        else:
            color = (0, 255, 0)       # Green fallback

        label = (
            f"{detection.class_name} "
            f"{detection.confidence:.2f} "
            f"ID:{track.track_id}"
        )

        cv2.rectangle(
            output,
            (x1, y1),
            (x2, y2),
            color,
            3,
        )

        cv2.putText(
            output,
            label,
            (x1, max(25, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2,
            cv2.LINE_AA,
        )

    return output