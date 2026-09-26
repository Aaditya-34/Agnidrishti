from pathlib import Path
import re

root = Path("data")
ok = True

print("Dataset integrity check")
print("========================")

for split in ["train", "val"]:
    img_dir = root / "images" / split
    lbl_dir = root / "labels" / split

    images = list(img_dir.glob("*.jpg"))
    labels = list(lbl_dir.glob("*.txt"))

    print(f"{split}: {len(images)} images, {len(labels)} labels")

    for img in images:
        label = lbl_dir / f"{img.stem}.txt"
        if not label.exists():
            print(f"MISSING LABEL: {img.name}")
            ok = False

    for label in labels:
        for line_no, line in enumerate(label.read_text().splitlines(), 1):
            if not line.strip():
                continue

            parts = line.split()

            if len(parts) != 5:
                print(f"INVALID LABEL: {label} line {line_no}: expected 5 values")
                ok = False
                continue

            if parts[0] not in {"0", "1"}:
                print(f"INVALID CLASS: {label} line {line_no}: {parts[0]}")
                ok = False

            for value in parts[1:]:
                if not re.fullmatch(r"-?(?:\d+(?:\.\d*)?|\.\d+)", value):
                    print(f"INVALID VALUE: {label} line {line_no}: {value}")
                    ok = False

print("========================")
print("PASS" if ok else "FAIL")
