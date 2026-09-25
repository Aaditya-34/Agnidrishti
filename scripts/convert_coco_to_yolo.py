import json
import shutil
from pathlib import Path


CLASS_MAP = {
    1: 0,  # smoke
    2: 1,  # fire
}

SOURCE_DIR = Path("data/annotations/verified/coco")
FRAME_DIR = Path("data/frames")
OUTPUT_DIR = Path("data/dataset")


def convert_video(video_name: str) -> tuple[int, int]:
    coco_path = (
        SOURCE_DIR
        / video_name
        / "annotations"
        / "instances_default.json"
    )

    if not coco_path.exists():
        raise FileNotFoundError(f"Missing COCO file: {coco_path}")

    with coco_path.open("r", encoding="utf-8") as f:
        coco = json.load(f)

    images = {image["id"]: image for image in coco["images"]}

    annotations_by_image = {}
    for annotation in coco["annotations"]:
        annotations_by_image.setdefault(annotation["image_id"], []).append(
            annotation
        )

    image_source_dir = FRAME_DIR / video_name

    converted_images = 0
    converted_boxes = 0

    for image_id, image in images.items():
        file_name = Path(image["file_name"]).name
        source_image = image_source_dir / file_name

        if not source_image.exists():
            raise FileNotFoundError(
                f"Missing source image: {source_image}"
            )

        destination_image = (
            OUTPUT_DIR / "images" / "all" / f"{video_name}_{file_name}"
        )

        destination_label = (
            OUTPUT_DIR / "labels" / "all"
            / f"{video_name}_{Path(file_name).stem}.txt"
        )

        destination_image.parent.mkdir(parents=True, exist_ok=True)
        destination_label.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(source_image, destination_image)

        width = image["width"]
        height = image["height"]

        lines = []

        for annotation in annotations_by_image.get(image_id, []):
            category_id = annotation["category_id"]

            if category_id not in CLASS_MAP:
                raise ValueError(
                    f"Unknown category ID {category_id} in {coco_path}"
                )

            x, y, box_width, box_height = annotation["bbox"]

            if box_width <= 0 or box_height <= 0:
                raise ValueError(
                    f"Invalid bounding box in {coco_path}: "
                    f"{annotation['bbox']}"
                )

            x_center = (x + box_width / 2) / width
            y_center = (y + box_height / 2) / height
            normalized_width = box_width / width
            normalized_height = box_height / height

            values = [
                x_center,
                y_center,
                normalized_width,
                normalized_height,
            ]

            if not all(0 <= value <= 1 for value in values):
                raise ValueError(
                    f"Out-of-range YOLO coordinates for "
                    f"{video_name}/{file_name}: {values}"
                )

            class_id = CLASS_MAP[category_id]

            lines.append(
                f"{class_id} "
                f"{x_center:.6f} "
                f"{y_center:.6f} "
                f"{normalized_width:.6f} "
                f"{normalized_height:.6f}"
            )

            converted_boxes += 1

        destination_label.write_text(
            "\n".join(lines) + ("\n" if lines else ""),
            encoding="utf-8",
        )

        converted_images += 1

    return converted_images, converted_boxes


def main():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    total_images = 0
    total_boxes = 0

    for video_name in ("video_01", "video_02"):
        images, boxes = convert_video(video_name)

        print(
            f"{video_name}: "
            f"{images} images, {boxes} boxes converted"
        )

        total_images += images
        total_boxes += boxes

    print()
    print(f"Total images: {total_images}")
    print(f"Total boxes: {total_boxes}")
    print("YOLO class mapping: 0=smoke, 1=fire")


if __name__ == "__main__":
    main()