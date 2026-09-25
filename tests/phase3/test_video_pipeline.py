import cv2
import numpy as np

from scripts.inference.filtering import filter_detections
from scripts.inference.renderer import render_tracks
from scripts.inference.statistics import ConfidenceStatistics
from scripts.inference.test_detector import TestDetector
from scripts.inference.tracker import IoUTracker


def create_test_video(path, frame_count=10, width=320, height=240, fps=10):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        str(path),
        fourcc,
        fps,
        (width, height),
    )

    assert writer.isOpened()

    frame = np.zeros((height, width, 3), dtype=np.uint8)

    for _ in range(frame_count):
        writer.write(frame)

    writer.release()


def test_video_pipeline_produces_valid_output(tmp_path):
    input_path = tmp_path / "input.mp4"
    output_path = tmp_path / "output.mp4"
    statistics_path = tmp_path / "statistics.json"

    create_test_video(input_path)

    detector = TestDetector()
    tracker = IoUTracker()
    statistics = ConfidenceStatistics()

    input_capture = cv2.VideoCapture(str(input_path))

    assert input_capture.isOpened()

    fps = input_capture.get(cv2.CAP_PROP_FPS)
    width = int(input_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(input_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    assert fps > 0
    assert width > 0
    assert height > 0

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        (width, height),
    )

    assert writer.isOpened()

    processed_frames = 0

    while True:
        ret, frame = input_capture.read()

        if not ret:
            break

        detections = detector.detect(frame)

        filtered_detections = filter_detections(
            detections,
            confidence_threshold=0.50,
        )

        assert filtered_detections

        statistics.update(filtered_detections)

        tracks = tracker.update(filtered_detections)

        assert tracks

        annotated_frame = render_tracks(
            frame,
            tracks,
        )

        assert annotated_frame.shape == frame.shape

        writer.write(annotated_frame)

        processed_frames += 1

    input_capture.release()
    writer.release()

    assert processed_frames == 10
    assert output_path.exists()
    assert output_path.stat().st_size > 0

    output_capture = cv2.VideoCapture(str(output_path))

    assert output_capture.isOpened()

    output_width = int(
        output_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    )
    output_height = int(
        output_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    output_frames = int(
        output_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    assert output_width == width
    assert output_height == height
    assert output_frames == processed_frames

    output_capture.release()

    summary = statistics.summary()

    assert "test" in summary
    assert summary["test"]["detections"] == processed_frames
    assert summary["test"]["average_confidence"] == 0.90