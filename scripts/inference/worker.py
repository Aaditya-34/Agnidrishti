import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from scripts.run_video_inference import run_inference


@dataclass
class VideoProcessingResult:
    status: str
    output_video: Optional[str] = None
    statistics_file: Optional[str] = None
    smoke_detections: int = 0
    smoke_average_confidence: float = 0.0
    fire_detections: int = 0
    fire_average_confidence: float = 0.0
    processed_frames: int = 0
    error: Optional[str] = None


def process_video(
    input_video: str,
    model_path: str,
    output_video: str,
    statistics_file: str,
    confidence_threshold: float = 0.50,
    detector_type: str = "yolo",
) -> VideoProcessingResult:
    """
    Process a video through the existing model-agnostic inference pipeline.

    This function is intended to be called by a backend/worker service.
    """

    try:
        run_inference(
            input_path=input_video,
            model_path=model_path,
            output_path=output_video,
            statistics_path=statistics_file,
            confidence_threshold=confidence_threshold,
            detector_type=detector_type,
        )

        statistics_path = Path(statistics_file)

        if not statistics_path.exists():
            raise RuntimeError(
                f"Statistics file was not created: {statistics_file}"
            )



        with statistics_path.open("r", encoding="utf-8") as file:
            summary = json.load(file)

        per_class = summary.get("per_class", {})

        smoke = per_class.get("smoke", {})
        fire = per_class.get("fire", {})

        return VideoProcessingResult(
            status="completed",
            output_video=str(output_video),
            statistics_file=str(statistics_file),
            smoke_detections=int(smoke.get("detections", 0)),
            smoke_average_confidence=float(
                smoke.get("average_confidence", 0.0)
            ),
            fire_detections=int(fire.get("detections", 0)),
            fire_average_confidence=float(
                fire.get("average_confidence", 0.0)
            ),
            processed_frames=int(
                summary.get("processed_frames", 0)
            ),
        )

    except Exception as exc:
        return VideoProcessingResult(
            status="failed",
            error=str(exc),
        )
