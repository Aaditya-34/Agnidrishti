# Reliability Analysis — M2

## Selected Model

- Model: YOLOv8n
- Input size: 960
- Training split: Experimental mixed-video split
- Training epochs: 50
- Classes: smoke, fire
- Checkpoint: `runs/detect/runs/detect/yolov8n_960_mixed/weights/best.pt`

## Independent Validation

The selected checkpoint was independently evaluated on the mixed validation split.

| Metric | Result |
|---|---:|
| Precision | 0.714 |
| Recall | 0.592 |
| mAP50 | 0.645 |
| mAP50-95 | 0.407 |

The independent validation results are consistent with the training-recorded metrics.

## Training Stability

| Epoch | Precision | Recall | mAP50 | mAP50-95 |
|---:|---:|---:|---:|---:|
| 46 | 0.702 | 0.567 | 0.634 | 0.403 |
| 47 | 0.680 | 0.557 | 0.631 | 0.402 |
| 48 | 0.680 | 0.576 | 0.636 | 0.404 |
| 49 | 0.725 | 0.592 | 0.644 | 0.408 |
| 50 | 0.732 | 0.570 | 0.638 | 0.405 |

The best mAP50-95 in the final training region occurred at epoch 49. Epoch 50 remained close to the preceding epochs.

## Confidence Behavior

Prediction confidence was collected on the 34-image mixed validation split using an initial prediction threshold of 0.001. This deliberately low threshold was used to observe confidence behavior.

- Total detections: 10,185
- Minimum confidence: 0.0010
- Maximum confidence: 0.9680
- Mean confidence: 0.0108
- Median confidence: 0.00166

The low mean and median are expected because the collection threshold was deliberately set to 0.001.

### Confidence Distribution by Class

| Class | Detections | Mean Confidence | Median Confidence | Maximum Confidence |
|---|---:|---:|---:|---:|
| Smoke | 6,504 | 0.0127 | 0.00183 | 0.9591 |
| Fire | 3,681 | 0.00754 | 0.00154 | 0.9680 |

### Detections Above Confidence Thresholds

| Confidence threshold | Overall | Smoke | Fire |
|---:|---:|---:|---:|
| >= 0.25 | 82 | 58 | 24 |
| >= 0.50 | 53 | 35 | 18 |
| >= 0.75 | 30 | 16 | 14 |
| >= 0.90 | 14 | 6 | 8 |

These are detection counts, not precision or recall values at the corresponding thresholds.

## Reliability Observations

1. Validation metrics remain relatively stable during the final training epochs.
2. Independent validation reproduces approximately the same overall performance as the recorded validation metrics.
3. The model produces both low-confidence and high-confidence predictions.
4. Increasing the confidence threshold substantially reduces retained detections.
5. Both smoke and fire have predictions reaching high confidence values.
6. Confidence alone is not sufficient to determine whether a detection is correct; it must be interpreted together with false positives, false negatives, and localization errors.

## Known Failure Modes

The error analysis identified:

- Missed smoke detections.
- Missed fire detections.
- False-positive smoke detections.
- Occasionally imprecise or overly broad smoke localization.
- Overlapping or duplicate detections in some frames.
- Difficult visual conditions where localization is inconsistent.

The confusion matrix also showed missed smoke and fire instances and background false positives.

## Overall Reliability Assessment

The selected YOLOv8n 960 mixed model provides measurable smoke and fire detection performance on the experimental mixed-video validation split and shows stable behavior near the end of training.

The validation results and error analysis also demonstrate documented limitations, including false positives, false negatives, localization errors, and confidence-dependent detection behavior.

Reliability evidence should therefore be considered together with quantitative metrics, the confusion matrix, prediction examples, and error analysis rather than confidence scores alone.

## Evidence Artifacts

- Training results: `runs/detect/runs/detect/yolov8n_960_mixed/results.csv`
- Training curves: `runs/detect/runs/detect/yolov8n_960_mixed/results.png`
- Confusion matrix: `runs/detect/runs/detect/yolov8n_960_mixed/confusion_matrix.png`
- Validation predictions: `runs/detect/runs/detect/yolov8n_960_mixed/val_batch*_pred.jpg`
- Validation labels: `runs/detect/runs/detect/yolov8n_960_mixed/val_batch*_labels.jpg`
- Error analysis: `reports/training/error_analysis.md`
- Selected checkpoint: `runs/detect/runs/detect/yolov8n_960_mixed/weights/best.pt`
