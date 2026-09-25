# Agnidrishti — YOLOv8 Baseline Results

## Dataset

- Total images: 164
- Total verified boxes: 484
- Smoke: 300
- Fire: 184
- Train: 96 images from video_01
- Validation: 68 images from video_02
- Classes:
  - 0 = smoke
  - 1 = fire
- Dataset QA: 0 invalid/out-of-range boxes

## Baseline Experiments

### YOLOv8n — 640px

Validation:
- Precision: 0.00401
- Recall: 0.79286
- mAP50: 0.01062
- mAP50-95: 0.00304

Training-split evaluation:
- Precision: 0.00478
- Recall: 0.38235
- mAP50: 0.00712
- mAP50-95: 0.00200

### YOLOv8n — 960px

Best training epoch: 38

Best recorded training-validation metric row:
- Precision: 0.1069
- Recall: 0.1000
- mAP50: 0.02025
- mAP50-95: 0.00344

Validation evaluation of best.pt:
- Precision: 0.09565
- Recall: 0.10714
- mAP50: 0.02272
- mAP50-95: 0.00368

Training-split evaluation of best.pt:
- Precision: 0.83383
- Recall: 0.59204
- mAP50: 0.75443
- mAP50-95: 0.52743

Per-class validation:
- Smoke: Precision 0.127, Recall 0.0714, mAP50 0.0296, mAP50-95 0.00572
- Fire: Precision 0.0641, Recall 0.143, mAP50 0.0158, mAP50-95 0.00163

### YOLOv8s — 960px

Validation evaluation of best.pt:
- Precision: 0.53307
- Recall: 0.01429
- mAP50: 0.00517
- mAP50-95: 0.00104

Per-class validation:
- Smoke: Precision 0.0661, Recall 0.0286, mAP50 0.0103, mAP50-95 0.00208
- Fire: Precision 1.000, Recall 0.000, mAP50 0.000, mAP50-95 0.000

## Generalization Observation

YOLOv8n-960 shows a substantial train-validation gap.

Training-split evaluation:
- mAP50: 0.75443
- mAP50-95: 0.52743

Validation-split evaluation:
- mAP50: 0.02272
- mAP50-95: 0.00368

The training data consists entirely of video_01 while validation consists entirely of video_02. Therefore, the observed gap is consistent with poor cross-video generalization.

The dataset should not be modified based solely on this observation. The verified annotations remain the source of truth.

## Artifacts

YOLOv8n-640:
- runs/detect/runs/detect/baseline_yolov8n-2/

YOLOv8n-960:
- runs/detect/runs/detect/baseline_yolov8n_960/

YOLOv8s-960:
- runs/detect/runs/detect/yolov8s_960/

Validation artifacts:
- runs/detect/val-5/
- runs/detect/val-7/
- runs/detect/val-8/
- runs/detect/val-9/

## Environment

- Python 3.12.9
- PyTorch 2.14.0+cu126
- Ultralytics 8.4.163
- NVIDIA GeForce RTX 3050 6GB Laptop GPU
- CUDA available: True
## Cross-video distribution analysis

The train/validation split is video-level: video_01 is used for training and video_02 for validation. Measured differences include:
- Brightness: mean pixel value 38.95 (train) vs 114.75 (validation).
- Image geometry: train images are 1080x1920 portrait; validation images are 1920x1080 landscape.
- Object scale: median normalized box area is 0.01868 (train) vs 0.13674 (validation), about 7.3x larger in validation.
- Class-specific scale: smoke median box area is 0.01547 (train) vs 0.11692 (validation); fire is 0.02150 vs 0.20509.

These measurements indicate substantial cross-video distribution shift. Therefore, the poor validation metrics should be interpreted as a cross-video generalization result rather than solely as an optimization or annotation-quality issue. The verified annotations remain the source of truth.

## YOLOv8n 960 augmentation experiment

Configuration:
- Architecture: YOLOv8n
- Image size: 960
- Epochs: 50
- Batch size: 4
- Augmentation: horizontal flip 0.5, rotation 10 degrees, translation 0.1, scale 0.5, HSV augmentation (h=0.015, s=0.7, v=0.4)
- Validation split: video_02

Results:
- Precision: 0.1800
- Recall: 0.0500
- mAP50: 0.0177
- mAP50-95: 0.00389

The augmentation experiment increased precision and slightly increased mAP50-95 relative to the YOLOv8n 960 baseline, but reduced recall and mAP50. Therefore, it is not a clear overall improvement on the current cross-video validation split.

Artifact:
- runs/detect/runs/detect/yolov8n_960_aug/weights/best.pt

## Final Mixed-Video Experiment

Experimental mixed split:
- Train: 130 images (76 video_01, 54 video_02)
- Validation: 34 images (20 video_01, 14 video_02)
- Random seed: 42

YOLOv8n, 960px, 50 epochs:
- Mixed validation Precision: 0.718
- Recall: 0.592
- mAP50: 0.644
- mAP50-95: 0.408

Evaluation on the original official video_02 validation set:
- 68 images, 84 instances
- Precision: 0.466
- Recall: 0.591
- mAP50: 0.561
- mAP50-95: 0.289

The official video_01-to-video_02 experiment remains the pure cross-video evaluation. The mixed experiment is reported separately because video_02 was included in training.

Selected M2 checkpoint:
runs/detect/runs/detect/yolov8n_960_mixed/weights/best.pt
