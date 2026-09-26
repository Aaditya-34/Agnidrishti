from pathlib import Path
import cv2


RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/metadata/temporal_preview")

INTERVAL_SECONDS = 10


def extract_preview(video_path):
    output_dir = OUTPUT_DIR / video_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print(f"ERROR: Could not open {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = frame_count / fps if fps > 0 else 0

    timestamp = 0.0
    extracted = 0

    while timestamp <= duration:
        cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)

        ret, frame = cap.read()

        if not ret:
            print(f"Warning: Could not read frame at {timestamp:.1f}s")
            timestamp += INTERVAL_SECONDS
            continue

        filename = f"{video_path.stem}_t{timestamp:06.1f}s.jpg"
        output_path = output_dir / filename

        cv2.imwrite(
            str(output_path),
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 90],
        )

        extracted += 1
        timestamp += INTERVAL_SECONDS

    cap.release()

    print(
        f"{video_path.name}: "
        f"{extracted} preview frames extracted"
    )


def main():
    videos = sorted(RAW_DIR.glob("*.mp4"))

    if not videos:
        print("No MP4 files found.")
        return

    for video_path in videos:
        extract_preview(video_path)


if __name__ == "__main__":
    main()