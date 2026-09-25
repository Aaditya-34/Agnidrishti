from pathlib import Path
import random
import shutil

ROOT = Path("data/experimental_mixed")
IMG_TRAIN = ROOT / "images" / "train"
IMG_VAL = ROOT / "images" / "val"
LBL_TRAIN = ROOT / "labels" / "train"
LBL_VAL = ROOT / "labels" / "val"

random.seed(42)

images = list(IMG_TRAIN.glob("*.jpg"))

# Group by source video
video_01 = [p for p in images if "video_01_" in p.name]
video_02 = [p for p in images if "video_02_" in p.name]

def split_group(files):
    random.shuffle(files)
    n = max(1, int(len(files) * 0.8))
    return files[:n], files[n:]

train_01, val_01 = split_group(video_01)
train_02, val_02 = split_group(video_02)

train_files = train_01 + train_02
val_files = val_01 + val_02

for img in val_files:
    label = LBL_TRAIN / (img.stem + ".txt")

    shutil.move(str(img), str(IMG_VAL / img.name))

    if label.exists():
        shutil.move(str(label), str(LBL_VAL / label.name))

print(f"Total images: {len(images)}")
print(f"Train images: {len(train_files)}")
print(f"Val images: {len(val_files)}")
print(f"Video 01 -> train: {len(train_01)}, val: {len(val_01)}")
print(f"Video 02 -> train: {len(train_02)}, val: {len(val_02)}")
