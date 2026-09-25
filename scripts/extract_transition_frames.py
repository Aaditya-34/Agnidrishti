from pathlib import Path

import cv2


RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/frames/transition_review")

SEGMENTS = {
    "video_01": [
        (8, 12),    # smoke appearance
        (28, 32),   # fire appearance
    ],
    "video_02": [
        (28, 32),   # smoke appearance
        (38, 42),   # stronger smoke
        (48, 52),   # fire appearance
        (78, 82),   # smoke transition
        (88, 92),   # fire + smoke transition
        (98, 102),  # smoke transition
    ],
}


def extract_segment(video_id, start_time, end_time):
    video_path = RAW_DIR / f"{video_id}.mp4"
    output_dir = OUTPUT_DIR / video_id
    output_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError(f"Could not open {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        raise RuntimeError(f"Invalid FPS for {video_path}")

    current_time = start_time
    extracted = 0

    while current_time <= end_time:
        cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)

        ret, frame = cap.read()

        if not ret:
            print(f"Warning: could not read {video_id} at {current_time:.3f}s")
            current_time += 1.0
            continue

        actual_frame_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

        filename = (
            f"{video_id}_transition_t"
            f"{actual_frame_time:09.3f}.jpg"
        )

        output_path = output_dir / filename

        success = cv2.imwrite(
            str(output_path),
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 95],
        )

        if success:
            extracted += 1

        current_time += 1.0

    cap.release()

    return extracted


def main():
    total = 0

    for video_id, segments in SEGMENTS.items():
        for start_time, end_time in segments:
            count = extract_segment(
                video_id,
                start_time,
                end_time,
            )

            print(
                f"{video_id}: "
                f"{start_time}s-{end_time}s -> "
                f"{count} frames"
            )

            total += count

    print(f"\nTotal transition-review frames: {total}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()