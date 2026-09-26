# Agnidrishti — YOLOv8n Error Analysis

## Selected Model

- Architecture: YOLOv8n
- Image size: 960px
- Training: 50 epochs
- Dataset: experimental mixed-video split
- Validation: 34 images, 111 instances
- Checkpoint: `runs/detect/runs/detect/yolov8n_960_mixed/weights/best.pt`

## Quantitative Error Evidence

The validation confusion matrix for the selected model shows:

| Predicted \ True | Smoke | Fire | Background |
|---|---:|---:|---:|
| Smoke | 41 | 0 | 22 |
| Fire | 0 | 21 | 2 |
| Background | 35 | 14 | — |

Observed errors:

- 35 smoke instances were missed and assigned to background.
- 14 fire instances were missed and assigned to background.
- 22 background instances were incorrectly predicted as smoke.
- 2 background instances were incorrectly predicted as fire.
- The matrix does not show direct smoke-to-fire or fire-to-smoke cross-class errors in these displayed counts.

## Visual Error Analysis

Validation prediction and ground-truth montages were inspected together.

### Correct detections

- A clear flame example was correctly classified as fire and localized over the visible flame region.
- Multiple smoke examples were correctly classified as smoke across several validation frames.
- Smoke was detected across consecutive frames containing visible smoke plumes.

### False negatives

- A validation frame containing visible flames has ground-truth fire annotations but no corresponding displayed prediction. This provides a concrete fire false-negative example.
- The confusion matrix quantitatively confirms missed instances for both smoke and fire.

### Localization errors

- Several smoke predictions cover a broader region than the corresponding ground-truth smoke annotation.
- This indicates that the class can be identified while the predicted bounding-box extent remains imprecise.

### Duplicate or overlapping detections

- Some validation prediction panels contain overlapping smoke predictions around the same plume.
- These examples indicate imperfect duplicate suppression/localization behavior in the displayed predictions.

### Confidence behavior

- Several displayed predictions have confidence values around 0.3–0.4.
- These examples indicate that some visually detectable smoke/fire cases are predicted with relatively low confidence.
- Confidence observations here are based on the displayed validation prediction montage and should not be interpreted as a global confidence distribution.

## Main Failure Modes

1. Missed smoke instances.
2. Missed fire instances.
3. Background regions incorrectly classified as smoke.
4. Smaller number of background regions incorrectly classified as fire.
5. Broad smoke bounding boxes.
6. Overlapping/duplicate smoke predictions.
7. Relatively low-confidence predictions in several visual examples.

## Interpretation

The selected YOLOv8n model demonstrates the ability to detect and localize both smoke and fire, including clear fire and repeated smoke examples. The principal observed limitations are missed detections, especially smoke, background-to-smoke false positives, and imperfect smoke localization.

These observations are reported as limitations of the trained model on the evaluated validation split. They do not imply that the verified annotations should be changed.

## Evidence Artifacts

- `runs/detect/runs/detect/yolov8n_960_mixed/confusion_matrix.png`
- `runs/detect/runs/detect/yolov8n_960_mixed/confusion_matrix_normalized.png`
- `runs/detect/runs/detect/yolov8n_960_mixed/val_batch0_labels.jpg`
- `runs/detect/runs/detect/yolov8n_960_mixed/val_batch0_pred.jpg`
- `runs/detect/runs/detect/yolov8n_960_mixed/BoxPR_curve.png`
- `runs/detect/runs/detect/yolov8n_960_mixed/BoxP_curve.png`
- `runs/detect/runs/detect/yolov8n_960_mixed/BoxR_curve.png`
- `runs/detect/runs/detect/yolov8n_960_mixed/BoxF1_curve.png`
