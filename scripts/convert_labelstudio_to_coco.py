import json
from pathlib import Path

from PIL import Image


INPUT = Path(
    "data/annotations/candidates/labelstudio/"
    "video_01_video_02_annotations.json"
)

OUTPUT_DIR = Path(
    "data/annotations/candidates/coco"
)

VIDEOS = {
    "video_01": Path("data/frames/video_01"),
    "video_02": Path("data/frames/video_02"),
}

# COCO category IDs
# Final YOLO mapping remains:
# 0 = smoke
# 1 = fire
CATEGORIES = [
    {
        "id": 1,
        "name": "smoke",
        "supercategory": "fire_smoke",
    },
    {
        "id": 2,
        "name": "fire",
        "supercategory": "fire_smoke",
    },
]

LABEL_TO_CATEGORY = {
    "smoke": 1,
    "fire": 2,
}


def load_input():
    with INPUT.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_local_filename(file_upload, frame_files):
    """
    Convert a Label Studio filename such as:

        93468e60-video_01_t00186.000.jpg

    into the local filename:

        video_01_t00186.000.jpg
    """

    filename = Path(file_upload).name

    # Exact match first.
    if filename in frame_files:
        return filename

    # Label Studio may prepend a UUID.
    matches = [
        local_name
        for local_name in frame_files
        if filename.endswith(local_name)
    ]

    if len(matches) == 1:
        return matches[0]

    return None


def get_label(result):
    labels = result.get("value", {}).get(
        "rectanglelabels", []
    )

    if not labels:
        return None

    return labels[0].strip().lower()


def convert_video(items, video_name, frame_dir):

    output = {
        "info": {
            "description":
                f"Agnidrishti M4 candidate annotations for {video_name}"
        },
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": CATEGORIES,
    }

    frame_files = {
        path.name: path
        for path in frame_dir.glob("*.jpg")
    }

    print(f"  Local frames: {len(frame_files)}")

    annotation_id = 1
    image_id = 1
    matched_frames = 0

    for item in items:

        file_upload = item.get("file_upload")

        if not file_upload:
            continue

        filename = get_local_filename(
            file_upload,
            frame_files,
        )

        if filename is None:
            print(
                "WARNING: frame not found locally:",
                Path(file_upload).name,
            )
            continue

        image_path = frame_files[filename]

        # Read actual image dimensions.
        with Image.open(image_path) as img:
            width, height = img.size

        output["images"].append({
            "id": image_id,
            "file_name": filename,
            "width": width,
            "height": height,
        })

        matched_frames += 1

        for annotation in item.get("annotations", []):

            for result in annotation.get("result", []):

                if result.get("type") != "rectanglelabels":
                    continue

                label = get_label(result)

                if label not in LABEL_TO_CATEGORY:
                    print(
                        f"WARNING: unknown label "
                        f"'{label}' in {filename}"
                    )
                    continue

                value = result.get("value", {})

                try:
                    x_percent = float(value["x"])
                    y_percent = float(value["y"])
                    w_percent = float(value["width"])
                    h_percent = float(value["height"])
                except (KeyError, TypeError, ValueError):
                    print(
                        f"WARNING: malformed bbox in {filename}"
                    )
                    continue

                # Label Studio percentages -> pixels.
                x = x_percent / 100.0 * width
                y = y_percent / 100.0 * height
                w = w_percent / 100.0 * width
                h = h_percent / 100.0 * height

                # Clamp bbox to image boundaries.
                x = max(0.0, min(x, width))
                y = max(0.0, min(y, height))

                w = max(0.0, min(w, width - x))
                h = max(0.0, min(h, height - y))

                if w <= 0 or h <= 0:
                    print(
                        f"WARNING: invalid bbox in {filename}: "
                        f"{x}, {y}, {w}, {h}"
                    )
                    continue

                output["annotations"].append({
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": LABEL_TO_CATEGORY[label],
                    "bbox": [
                        round(x, 3),
                        round(y, 3),
                        round(w, 3),
                        round(h, 3),
                    ],
                    "area": round(w * h, 3),
                    "iscrowd": 0,
                })

                annotation_id += 1

        image_id += 1

    print(f"  Matched local frames: {matched_frames}")
    print(
        f"  COCO images: {len(output['images'])}"
    )
    print(
        f"  COCO annotations: "
        f"{len(output['annotations'])}"
    )

    return output


def main():

    if not INPUT.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT}"
        )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = load_input()

    print(
        f"Input Label Studio records: {len(data)}"
    )

    for video_name, frame_dir in VIDEOS.items():

        items = []

        for item in data:

            file_upload = item.get(
                "file_upload",
                "",
            )

            filename = Path(file_upload).name

            if video_name + "_" in filename:
                items.append(item)

        print()
        print(f"{video_name}:")
        print(
            f"  Label Studio frames: "
            f"{len(items)}"
        )

        coco = convert_video(
            items,
            video_name,
            frame_dir,
        )

        output_file = (
            OUTPUT_DIR /
            f"{video_name}_candidates.json"
        )

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                coco,
                f,
                indent=2,
            )

        print(
            f"  Written: {output_file}"
        )


if __name__ == "__main__":
    main()