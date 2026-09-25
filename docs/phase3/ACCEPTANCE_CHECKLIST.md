# Agnidrishti Phase 3 Acceptance Checklist

## Purpose

This checklist defines the acceptance criteria for the complete Agnidrishti Phase 3 system.

Each item should be marked:

- [ ] Not tested
- [x] Passed
- [ ] Failed
- [ ] Blocked

A blocked item must include the dependency that prevents execution.

---

# 1. Backend / API

## Video Upload

- [ ] Valid MP4 upload is accepted.
- [ ] Invalid/non-video file is rejected.
- [ ] Missing file is rejected.
- [ ] Oversized file is rejected when an upload-size limit is configured.
- [ ] Appropriate error responses are returned for invalid uploads.

## Job Management

- [ ] Valid processing job can be created.
- [ ] Job ID is returned after creation.
- [ ] Processing status can be retrieved.
- [ ] Completed status can be retrieved.
- [ ] Failed status can be retrieved.
- [ ] Invalid/nonexistent job IDs are handled correctly.

## Output and Statistics APIs

- [ ] Completed output video can be retrieved.
- [ ] Completed-job statistics can be retrieved.
- [ ] Output retrieval fails safely when output does not exist.
- [ ] Statistics retrieval fails safely when statistics do not exist.

---

# 2. Video Processing

- [ ] Valid input video can be opened.
- [ ] Invalid/corrupt video is rejected.
- [ ] FPS is validated.
- [ ] Video width is valid.
- [ ] Video height is valid.
- [ ] Frames can be read successfully.
- [ ] Frames are processed without unexpected termination.
- [ ] Output video is generated.
- [ ] Output video is non-empty.
- [ ] Output video contains processed frames.
- [ ] Output video has valid dimensions.
- [ ] Output video is playable.
- [ ] No corrupted output video is produced.

---

# 3. Inference

## Model-Independent Pipeline

- [ ] Detector interface can be instantiated.
- [ ] TestDetector produces deterministic detections.
- [ ] Detection objects contain class ID.
- [ ] Detection objects contain class name.
- [ ] Detection objects contain confidence.
- [ ] Detection objects contain bounding-box coordinates.
- [ ] Confidence filtering works.
- [ ] IoU tracking works.
- [ ] Track IDs are generated.
- [ ] Track IDs remain reasonably stable for consecutive overlapping detections.
- [ ] Different classes are not incorrectly matched.

## YOLO Model

These items require the final M2 `.pt` model.

- [ ] YOLO model loads successfully.
- [ ] Smoke predictions are produced correctly.
- [ ] Fire predictions are produced correctly.
- [ ] Confidence values are produced.
- [ ] Bounding boxes are produced.
- [ ] Inference failure is handled safely.
- [ ] Missing model file is handled safely.

---

# 4. Output Video

- [ ] Output MP4 exists.
- [ ] Output MP4 is non-empty.
- [ ] Output MP4 can be opened.
- [ ] Output MP4 can be decoded.
- [ ] Output dimensions are valid.
- [ ] Processed frames are present.
- [ ] Bounding boxes are rendered.
- [ ] Class labels are rendered.
- [ ] Confidence scores are displayed.
- [ ] Track IDs are displayed when tracking is enabled.
- [ ] Smoke bounding boxes are visually correct.
- [ ] Fire bounding boxes are visually correct.
- [ ] Multiple detections are rendered correctly.
- [ ] No corrupted or empty output is produced.

Smoke/fire visual checks require the final M2 model.

---

# 5. Statistics

- [ ] Detection counts are available.
- [ ] Smoke detection count is available.
- [ ] Fire detection count is available.
- [ ] Average smoke confidence is calculated.
- [ ] Average fire confidence is calculated.
- [ ] Maximum confidence is calculated where applicable.
- [ ] Minimum confidence is calculated where applicable.
- [ ] No-detection cases are handled safely.
- [ ] Statistics JSON is generated.
- [ ] Statistics correspond to the processed video.
- [ ] Statistics can be retrieved through the backend once implemented.

---

# 6. Error Handling

- [ ] Missing input file is handled.
- [ ] Invalid video file is handled.
- [ ] Unsupported file type is handled.
- [ ] Oversized file is handled when a size limit exists.
- [ ] Invalid job ID is handled.
- [ ] Video-open failure is handled.
- [ ] Invalid FPS is handled.
- [ ] Invalid dimensions are handled.
- [ ] Output-video creation failure is handled.
- [ ] Inference failure is handled.
- [ ] Statistics-generation failure is handled.
- [ ] Failed jobs are not reported as completed.
- [ ] Error information is sufficiently clear for debugging.

---

# 7. Dashboard

These checks require the planned React frontend and backend integration.

- [ ] Uploaded video/job appears in the dashboard.
- [ ] Processing state is displayed.
- [ ] Completed state is displayed.
- [ ] Failed state is displayed.
- [ ] Output video can be accessed from the dashboard.
- [ ] Detection statistics are displayed.
- [ ] Smoke statistics are displayed.
- [ ] Fire statistics are displayed.
- [ ] Backend errors are represented appropriately.

M4 does not implement the React frontend.

---

# 8. Model-Output Quality

These checks require the final M2 `.pt` model.

## Classification

- [ ] Smoke is classified as smoke.
- [ ] Fire is classified as fire.
- [ ] Smoke/fire confusion is evaluated.
- [ ] Difficult mixed smoke/fire scenes are evaluated.

## Detection Quality

- [ ] False positives are evaluated.
- [ ] False negatives are evaluated.
- [ ] Small/distant smoke is evaluated.
- [ ] Fire detection misses are evaluated.
- [ ] Bounding-box quality is evaluated.
- [ ] Confidence behavior is evaluated.

## Temporal Behavior

- [ ] Consecutive-frame detection stability is evaluated.
- [ ] Bounding-box flickering is evaluated.
- [ ] Track-ID stability is evaluated.
- [ ] Difficult temporal scenes are evaluated.

---

# 9. Reference Annotations

- [ ] Verified annotations are used as reference for model-output QA where appropriate.
- [ ] Verified annotations are not modified to improve model results.
- [ ] Model predictions are evaluated against the existing verified reference.
- [ ] Ambiguous cases are documented rather than changing the reference labels.

---

# 10. QA Separation

## Automated QA

- [ ] Automated tests are implemented for deterministic behavior.
- [ ] Automated tests are repeatable.
- [ ] Automated tests can run without the final M2 model wherever possible.

## Manual Visual QA

- [ ] Output videos are manually inspected.
- [ ] Bounding boxes are visually inspected.
- [ ] Class labels are visually inspected.
- [ ] Confidence labels are visually inspected.
- [ ] Track behavior is visually inspected.
- [ ] Difficult scenes are visually inspected.

## Model Performance Evaluation

- [ ] Final model is evaluated separately from system/integration QA.
- [ ] False positives are recorded.
- [ ] False negatives are recorded.
- [ ] Classification errors are recorded.
- [ ] Localization errors are recorded.
- [ ] Temporal errors are recorded.

---

# 11. Phase 3 Dependency Status

| Area | Dependency | Status |
|---|---|---|
| QA documentation | Repository architecture | Available |
| Automated pipeline QA | Test detector | Available |
| Video-output QA | Test video | Required |
| Backend/API QA | FastAPI backend | Pending |
| Dashboard QA | React + backend integration | Pending |
| Model-quality QA | M2 final `.pt` | Pending |
| Verified-reference evaluation | Verified annotations | Available |
| End-to-end system QA | Backend + inference + dashboard | Pending |

---

# 12. Known Issues During QA Preparation

## QA-002

The inference entry point imports the YOLO detector implementation, which requires the Ultralytics package even when the test detector is intended to be used.

Status: Open

---

# 13. Final Acceptance

Phase 3 can be considered ready for final system acceptance when:

- [ ] Backend/API tests pass.
- [ ] Video processing tests pass.
- [ ] Inference pipeline tests pass.
- [ ] Output-video tests pass.
- [ ] Statistics tests pass.
- [ ] Error-handling tests pass.
- [ ] Dashboard integration tests pass.
- [ ] Manual visual QA is complete.
- [ ] Final M2 model-output evaluation is complete.
- [ ] Model-quality findings are documented.
- [ ] No critical/blocking defects remain unresolved.
- [ ] Verified annotations remain unchanged.
- [ ] M4 QA work remains isolated from M2 training and frontend implementation.