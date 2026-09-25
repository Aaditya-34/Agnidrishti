from pathlib import Path
import cv2


RAW_DIR = Path("data/raw")


def get_codec(cap):
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))

    if fourcc == 0:
        return "UNKNOWN"

    return "".join(
        chr((fourcc >> (8 * i)) & 0xFF)
        for i in range(4)
    )


def inspect_video(video_path):
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print(f"ERROR: Could not open {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    codec = get_codec(cap)

    duration = frame_count / fps if fps > 0 else 0

    print("=" * 70)
    print(f"File        : {video_path.name}")
    print(f"Duration    : {duration:.3f} seconds")
    print(f"Resolution  : {width} x {height}")
    print(f"FPS         : {fps:.3f}")
    print(f"Frame count : {frame_count}")
    print(f"Codec       : {codec}")
    print("=" * 70)

    cap.release()


def main():
    videos = sorted(RAW_DIR.glob("*.mp4"))

    if not videos:
        print(f"No MP4 files found in {RAW_DIR}")
        return

    print(f"Found {len(videos)} MP4 file(s).\n")

    for video_path in videos:
        inspect_video(video_path)


if __name__ == "__main__":
    main()