from pathlib import Path
import csv
import re


FRAMES_DIR = Path("data/frames")
OUTPUT_PATH = Path("data/manifests/frames.csv")


FRAME_PATTERN = re.compile(
    r"^(?P<video>.+)_t(?P<timestamp>\d+\.\d+)\.jpg$"
)


def collect_frames():
    rows = []

    for video_dir in sorted(FRAMES_DIR.iterdir()):
        if not video_dir.is_dir():
            continue

        for frame_path in sorted(video_dir.glob("*.jpg")):
            match = FRAME_PATTERN.match(frame_path.name)

            if not match:
                print(f"Skipping unexpected filename: {frame_path.name}")
                continue

            video_id = match.group("video")
            timestamp = float(match.group("timestamp"))

            rows.append(
                {
                    "frame_id": frame_path.stem,
                    "video_id": video_id,
                    "timestamp": timestamp,
                    "frame_path": str(frame_path).replace("\\", "/"),
                }
            )

    return rows


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = collect_frames()

    fieldnames = [
        "frame_id",
        "video_id",
        "timestamp",
        "frame_path",
    ]

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Manifest created: {OUTPUT_PATH}")
    print(f"Total frames: {len(rows)}")


if __name__ == "__main__":
    main()