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
