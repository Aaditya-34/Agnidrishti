import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

import imageio_ffmpeg

from scripts.run_video_inference import run_inference


ProgressCallback = Callable[[int, int], None]


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
    total_frames: int = 0

    error: Optional[str] = None


def convert_to_browser_mp4(
    input_video: str,
    output_video: str,
) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    command = [
        ffmpeg,
        "-y",
        "-i",
        input_video,
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "23",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-an",
        output_video,
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "FFmpeg H.264 conversion failed:\n"
            + result.stderr[-4000:]
        )


def process_video(
    input_video: str,
    model_path: str,
    output_video: str,
    statistics_file: str,
    confidence_threshold: float = 0.50,
    detector_type: str = "yolo",
    progress_callback: Optional[ProgressCallback] = None,
) -> VideoProcessingResult:
    try:
        raw_output = str(
            Path(output_video).with_name(
                Path(output_video).stem + "_raw.mp4"
            )
        )

        run_inference(
            input_path=input_video,
            model_path=model_path,
            output_path=raw_output,
            statistics_path=statistics_file,
            confidence_threshold=confidence_threshold,
            detector_type=detector_type,
            progress_callback=progress_callback,
        )

        convert_to_browser_mp4(
            input_video=raw_output,
            output_video=output_video,
        )

        raw_path = Path(raw_output)

        if raw_path.exists():
            raw_path.unlink()

        statistics_path = Path(statistics_file)

        if not statistics_path.exists():
            raise RuntimeError(
                f"Statistics file was not created: "
                f"{statistics_file}"
            )

        output_path = Path(output_video)

        if not output_path.exists():
            raise RuntimeError(
                "Browser-compatible output was not created: "
                f"{output_video}"
            )

        with statistics_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            summary = json.load(file)

        per_class = summary.get(
            "per_class",
            {},
        )

        smoke = per_class.get(
            "smoke",
            {},
        )

        fire = per_class.get(
            "fire",
            {},
        )

        return VideoProcessingResult(
            status="completed",
            output_video=str(output_video),
            statistics_file=str(statistics_file),

            smoke_detections=int(
                smoke.get("detections", 0)
            ),

            smoke_average_confidence=float(
                smoke.get(
                    "average_confidence",
                    0.0,
                )
            ),

            fire_detections=int(
                fire.get("detections", 0)
            ),

            fire_average_confidence=float(
                fire.get(
                    "average_confidence",
                    0.0,
                )
            ),

            processed_frames=int(
                summary.get(
                    "processed_frames",
                    0,
                )
            ),

            total_frames=int(
                summary.get(
                    "total_frames",
                    0,
                )
            ),
        )

    except Exception as exc:
        return VideoProcessingResult(
            status="failed",
            error=str(exc),
        )