from pathlib import Path
import cv2

ROOT = Path("data/dataset")

total_images = 0
total_labels = 0
total_boxes = 0
smoke = 0
fire = 0
errors = []

for split in ["train", "val"]:
    image_dir = ROOT / "images" / split
    label_dir = ROOT / "labels" / split

    images = list(image_dir.glob("*.jpg"))

    for image in images:
        total_images += 1

        if cv2.imread(str(image)) is None:
            errors.append(f"Unreadable image: {image}")

        label = label_dir / f"{image.stem}.txt"

        if not label.exists():
            errors.append(f"Missing label: {label}")
            continue

        total_labels += 1

        for line_number, line in enumerate(
            label.read_text(encoding="utf-8").splitlines(), 1
        ):
            if not line.strip():
                continue

            parts = line.split()

            if len(parts) != 5:
                errors.append(
                    f"Invalid format: {label}:{line_number}"
                )
                continue

            try:
                class_id = int(parts[0])
                values = [float(x) for x in parts[1:]]
            except ValueError:
                errors.append(
                    f"Invalid numbers: {label}:{line_number}"
                )
                continue

            if class_id not in [0, 1]:
                errors.append(
                    f"Invalid class {class_id}: {label}:{line_number}"
                )
                continue

            if not all(0 <= value <= 1 for value in values):
                errors.append(
                    f"Out-of-range box: {label}:{line_number}"
                )
                continue

            total_boxes += 1

            if class_id == 0:
                smoke += 1
            else:
                fire += 1


print("YOLO DATASET QA")
print("----------------")
print(f"Images: {total_images}")
print(f"Labels: {total_labels}")
print(f"Smoke boxes: {smoke}")
print(f"Fire boxes: {fire}")
print(f"Total boxes: {total_boxes}")
print(f"Errors: {len(errors)}")

if errors:
    print("\nErrors:")
    for error in errors[:20]:
        print(error)
else:
    print("\nQA PASSED")