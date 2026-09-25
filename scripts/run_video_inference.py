from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import argparse
import json

import cv2

from scripts.inference.filtering import filter_detections
from scripts.inference.renderer import render_tracks
from scripts.inference.statistics import ConfidenceStatistics
from scripts.inference.tracker import IoUTracker
from scripts.inference.yolo_detector import YOLODetector
from scripts.inference.test_detector import TestDetector


def run_inference(
    input_path: str,
    model_path: str,
    output_path: str,
    statistics_path: str,
    confidence_threshold: float,
    detector_type: str,
):
    input_path = Path(input_path)
    output_path = Path(output_path)
    statistics_path = Path(statistics_path)

    if not input_path.exists():
        raise FileNotFoundError(f'Input video not found: {input_path}')

    output_path.parent.mkdir(parents=True, exist_ok=True)
    statistics_path.parent.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(input_path))

    if not cap.isOpened():
        raise RuntimeError(f'Could not open input video: {input_path}')

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps <= 0:
        cap.release()
        raise RuntimeError('Invalid FPS detected')

    if width <= 0 or height <= 0:
        cap.release()
        raise RuntimeError('Invalid video dimensions')

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    writer = cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        (width, height),
    )

    if not writer.isOpened():
        cap.release()
        raise RuntimeError(f'Could not create output video: {output_path}')

    if detector_type == 'test':
        detector = TestDetector()
    elif detector_type == 'yolo':
        detector = YOLODetector(
            model_path=model_path,
            confidence_threshold=confidence_threshold,
        )
    else:
        cap.release()
        writer.release()
        raise ValueError(f'Unsupported detector type: {detector_type}')

    tracker = IoUTracker()
    statistics = ConfidenceStatistics()

    processed_frames = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        detections = detector.detect(frame)

        filtered_detections = filter_detections(
            detections,
            confidence_threshold=confidence_threshold,
        )

        statistics.update(filtered_detections)

        tracks = tracker.update(filtered_detections)

        annotated_frame = render_tracks(
            frame,
            tracks,
        )

        writer.write(annotated_frame)

        processed_frames += 1

        if processed_frames % 100 == 0:
            print(f'Processed {processed_frames}/{total_frames} frames')

    cap.release()
    writer.release()

    summary = {
        'input_video': str(input_path),
        'output_video': str(output_path),
        'detector': detector_type,
        'fps': fps,
        'width': width,
        'height': height,
        'total_frames': total_frames,
        'processed_frames': processed_frames,
        'confidence_threshold': confidence_threshold,
        'per_class': statistics.summary(),
    }

    with statistics_path.open('w', encoding='utf-8') as file:
        json.dump(summary, file, indent=2)

    print()
    print('Inference complete.')
    print(f'Input video : {input_path}')
    print(f'Output video: {output_path}')
    print(f'Statistics  : {statistics_path}')
    print(f'Detector    : {detector_type}')
    print(f'Frames      : {processed_frames}')


def main():
    parser = argparse.ArgumentParser(
        description='Run object detection on an input MP4.'
    )

    parser.add_argument(
        '--input',
        required=True,
        help='Input MP4 path',
    )

    parser.add_argument(
        '--model',
        default='',
        help='YOLO model .pt path. Not required for test detector.',
    )

    parser.add_argument(
        '--output',
        required=True,
        help='Output MP4 path',
    )

    parser.add_argument(
        '--statistics',
        required=True,
        help='Output statistics JSON path',
    )

    parser.add_argument(
        '--confidence',
        type=float,
        default=0.50,
        help='Confidence threshold',
    )

    parser.add_argument(
        '--detector',
        choices=['yolo', 'test'],
        default='yolo',
        help='Detector backend to use.',
    )

    args = parser.parse_args()

    if not 0.0 <= args.confidence <= 1.0:
        raise ValueError('Confidence threshold must be between 0 and 1.')

    if args.detector == 'yolo' and not args.model:
        raise ValueError(
            '--model is required when using the YOLO detector.'
        )

    run_inference(
        input_path=args.input,
        model_path=args.model,
        output_path=args.output,
        statistics_path=args.statistics,
        confidence_threshold=args.confidence,
        detector_type=args.detector,
    )


if __name__ == '__main__':
    main()
