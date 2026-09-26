from pathlib import Path
import argparse

import cv2


def extract_frames(input_path, output_dir, interval):
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(input_path))

    if not cap.isOpened():
        raise RuntimeError(f"Could not open {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        raise RuntimeError("Invalid FPS detected")

    frame_interval = max(1, round(fps * interval))

    frame_index = 0
    extracted = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_index % frame_interval == 0:
            timestamp = frame_index / fps

            output_name = (
                f"{input_path.stem}_"
                f"t{timestamp:09.3f}.jpg"
            )

            output_path = output_dir / output_name

            success = cv2.imwrite(
                str(output_path),
                frame,
                [cv2.IMWRITE_JPEG_QUALITY, 95],
            )

            if success:
                extracted += 1

        frame_index += 1

    cap.release()

    print(f"Input       : {input_path}")
    print(f"FPS         : {fps:.3f}")
    print(f"Interval    : {interval} seconds")
    print(f"Frames read : {frame_index}")
    print(f"Frames saved: {extracted}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract frames at a fixed time interval."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Input MP4 path",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output frame directory",
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Sampling interval in seconds",
    )

    args = parser.parse_args()

    if args.interval <= 0:
        raise ValueError("Interval must be greater than zero")

    extract_frames(
        args.input,
        args.output,
        args.interval,
    )


if __name__ == "__main__":
    main()