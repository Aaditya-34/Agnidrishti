import numpy as np

from scripts.inference.detector import Detection
from scripts.inference.filtering import filter_detections
from scripts.inference.test_detector import TestDetector


def test_test_detector_returns_detection():
    frame = np.zeros((480, 640, 3), dtype=np.uint8)

    detections = TestDetector().detect(frame)

    assert len(detections) == 1

    detection = detections[0]

    assert isinstance(detection, Detection)
    assert detection.class_id == 0
    assert detection.class_name == "test"
    assert detection.confidence == 0.90


def test_test_detector_bbox_is_inside_frame():
    frame = np.zeros((480, 640, 3), dtype=np.uint8)

    detection = TestDetector().detect(frame)[0]

    assert 0 <= detection.x1 < detection.x2 <= 640
    assert 0 <= detection.y1 < detection.y2 <= 480


def test_filter_removes_detection_below_threshold():
    detection = Detection(
        class_id=0,
        class_name="smoke",
        confidence=0.40,
        x1=10,
        y1=10,
        x2=100,
        y2=100,
    )

    result = filter_detections([detection], confidence_threshold=0.50)

    assert result == []


def test_filter_keeps_detection_at_threshold():
    detection = Detection(
        class_id=0,
        class_name="smoke",
        confidence=0.50,
        x1=10,
        y1=10,
        x2=100,
        y2=100,
    )

    result = filter_detections([detection], confidence_threshold=0.50)

    assert result == [detection]


def test_filter_keeps_detection_above_threshold():
    detection = Detection(
        class_id=1,
        class_name="fire",
        confidence=0.90,
        x1=10,
        y1=10,
        x2=100,
        y2=100,
    )

    result = filter_detections([detection], confidence_threshold=0.50)

    assert result == [detection]