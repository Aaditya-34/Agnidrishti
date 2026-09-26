# M3 Phase 3 - Video Inference Worker

## Purpose

The video inference worker provides a service-level interface around the existing model-agnostic video inference pipeline.

It allows the FastAPI backend to call video processing without depending on the CLI.

## Worker interface

```python
from scripts.inference.worker import process_video

result = process_video(
    input_video="data/raw/video_02.mp4",
    model_path="path/to/model.pt",
    output_video="data/inference/result.mp4",
    statistics_file="data/inference/result_stats.json",
    confidence_threshold=0.50,
    detector_type="yolo",
)