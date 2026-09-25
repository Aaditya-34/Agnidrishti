from dataclasses import dataclass
from typing import List

from .detector import Detection


@dataclass
class Track:
    track_id: int
    detection: Detection
    missed_frames: int = 0


class IoUTracker:
    """Lightweight IoU-based tracker for temporal detection stabilization."""

    def __init__(
        self,
        iou_threshold: float = 0.3,
        max_missed_frames: int = 5,
    ):
        self.iou_threshold = iou_threshold
        self.max_missed_frames = max_missed_frames
        self.next_track_id = 1
        self.tracks: List[Track] = []

    @staticmethod
    def _iou(a: Detection, b: Detection) -> float:
        x1 = max(a.x1, b.x1)
        y1 = max(a.y1, b.y1)
        x2 = min(a.x2, b.x2)
        y2 = min(a.y2, b.y2)

        intersection_width = max(0.0, x2 - x1)
        intersection_height = max(0.0, y2 - y1)
        intersection = intersection_width * intersection_height

        area_a = max(0.0, a.x2 - a.x1) * max(0.0, a.y2 - a.y1)
        area_b = max(0.0, b.x2 - b.x1) * max(0.0, b.y2 - b.y1)

        union = area_a + area_b - intersection

        if union <= 0:
            return 0.0

        return intersection / union

    def update(self, detections: List[Detection]) -> List[Track]:
        unmatched_tracks = set(range(len(self.tracks)))
        unmatched_detections = set(range(len(detections)))

        matches = []

        for track_index, track in enumerate(self.tracks):
            best_detection_index = None
            best_iou = 0.0

            for detection_index, detection in enumerate(detections):
                if detection_index not in unmatched_detections:
                    continue

                if track.detection.class_id != detection.class_id:
                    continue

                score = self._iou(track.detection, detection)

                if score > best_iou:
                    best_iou = score
                    best_detection_index = detection_index

            if (
                best_detection_index is not None
                and best_iou >= self.iou_threshold
            ):
                matches.append((track_index, best_detection_index))
                unmatched_tracks.discard(track_index)
                unmatched_detections.discard(best_detection_index)

        for track_index, detection_index in matches:
            self.tracks[track_index].detection = detections[detection_index]
            self.tracks[track_index].missed_frames = 0

        for track_index in unmatched_tracks:
            self.tracks[track_index].missed_frames += 1

        self.tracks = [
            track
            for track in self.tracks
            if track.missed_frames <= self.max_missed_frames
        ]

        for detection_index in unmatched_detections:
            self.tracks.append(
                Track(
                    track_id=self.next_track_id,
                    detection=detections[detection_index],
                )
            )
            self.next_track_id += 1

        return list(self.tracks)
