# Agnidrishti Phase 3 QA Plan

## 1. Purpose

This document defines the Phase 3 system QA and validation plan for Agnidrishti.

Phase 3 QA covers the complete intended workflow:

Upload video
→ create processing job
→ validate video
→ process video
→ run inference
→ generate output video
→ calculate statistics
→ complete job
→ display result on dashboard

The QA work is divided into:

1. Automated QA
2. Manual visual QA
3. Model-performance evaluation

Phase 3 QA preparation does not depend on the final M2 `.pt` model.

---

## 2. Scope

### In scope

- Video upload and validation
- Processing-job lifecycle
- Video processing
- Model-agnostic inference pipeline
- YOLO inference integration
- Detection filtering
- Temporal tracking
- Output-video rendering
- Detection statistics
- Backend/API behavior
- Error handling
- Dashboard result integration
- Final model-output evaluation

### Out of scope

- React frontend implementation
- M2 model training
- M2 training configuration
- Modification of verified annotations
- Modification of the verified dataset

---

## 3. Current Architecture

The current repository contains a model-agnostic video inference pipeline.

The intended flow is:

Input Video
→ Detector
→ Detection Filtering
→ Statistics
→ IoU Tracking
→ Output Rendering
→ Output MP4 + Statistics JSON

The detector interface supports different detector implementations.

Current detector implementations include:

- TestDetector
- YOLODetector

The test detector allows pipeline QA without requiring the final M2 model.

The project defines two detection classes:

| Class ID | Class |
|---|---|
| 0 | smoke |
| 1 | fire |

---

# 4. QA Categories

## 4.1 Automated QA

Automated tests should verify deterministic system behavior such as:

- API responses
- file validation
- job lifecycle
- video opening
- video metadata
- frame processing
- output-file creation
- output-video properties
- statistics structure
- error handling
- inference pipeline components

Automated QA should be repeatable and executable without the final YOLO model wherever possible.

## 4.2 Manual Visual QA

Manual inspection is required for visual behavior such as:

- bounding-box placement
- smoke labeling
- fire labeling
- confidence-label visibility
- track-ID behavior
- temporal stability
- output-video visual quality
- difficult or ambiguous scenes

## 4.3 Model-Performance Evaluation

Model-performance QA is performed after M2 provides the final `.pt` model.

The verified annotations are used as the reference where appropriate.

Verified annotations must not be modified to improve model results.

Model evaluation includes:

- smoke vs fire correctness
- false positives
- false negatives
- missed small/distant smoke
- missed fire
- smoke/fire confusion
- bounding-box quality
- confidence behavior
- difficult scenes
- temporal stability

---

# 5. Test Case Matrix

## 5.1 Backend/API Tests

| ID | Component | Input | Expected Result | Pass/Fail Criteria | Type | Execution |
|---|---|---|---|---|---|---|
| API-001 | Upload | Valid MP4 | Video accepted | Request succeeds and upload is accepted | Automated | Backend ready |
| API-002 | Upload | Non-video file | Upload rejected | Appropriate validation error returned | Automated | Backend ready |
| API-003 | Upload | Missing file | Request rejected | Appropriate client error returned | Automated | Backend ready |
| API-004 | Upload | Oversized file | Upload rejected when a limit exists | Configured size limit is enforced | Automated | Backend ready |
| API-005 | Job creation | Valid upload | Processing job created | Valid job ID returned | Automated | Backend ready |
| API-006 | Status | Valid job ID during processing | Processing status returned | Status represents processing state | Automated | Backend ready |
| API-007 | Status | Completed job | Completed status returned | Status represents successful completion | Automated | Backend ready |
| API-008 | Status | Failed job | Failed status returned | Failure state is exposed correctly | Automated | Backend ready |
| API-009 | Output retrieval | Completed job | Output available | Output can be retrieved | Automated | Backend ready |
| API-010 | Statistics | Completed job | Statistics available | Expected statistics are returned | Automated | Backend ready |
| API-011 | Job lookup | Invalid/nonexistent job ID | Request rejected | Appropriate not-found/error response | Automated | Backend ready |
| API-012 | Inference failure | Processing job with inference failure | Job fails safely | Failure state returned without false completion | Automated | Backend ready |

---

## 5.2 Video Processing Tests

| ID | Component | Input | Expected Result | Pass/Fail Criteria | Type | Execution |
|---|---|---|---|---|---|---|
| VID-001 | Input validation | Valid video | Video opens successfully | VideoCapture opens successfully | Automated | Now |
| VID-002 | Input validation | Invalid/corrupt video | Video rejected | Processing fails with controlled error | Automated | Now |
| VID-003 | Video metadata | Valid video | FPS available | FPS is greater than zero | Automated | Now |
| VID-004 | Video metadata | Valid video | Dimensions available | Width and height are greater than zero | Automated | Now |
| VID-005 | Frame processing | Valid video | Frames are read | Readable frames are processed | Automated | Now |
| VID-006 | Output | Processed video | MP4 created | Output file exists and is non-empty | Automated | Now |
| VID-007 | Output | Generated MP4 | Video playable | Video can be opened and decoded | Automated/Manual | Now |
| VID-008 | Output | Generated MP4 | Valid dimensions | Output dimensions are valid | Automated | Now |
| VID-009 | Output | Generated MP4 | No empty output | Output contains processed frames | Automated | Now |
| VID-010 | Frame consistency | Input/output video | Frame processing consistent | Processed frame count is consistent with pipeline behavior | Automated | Now |

---

## 5.3 Detection and Rendering Tests

| ID | Component | Input | Expected Result | Pass/Fail Criteria | Type | Execution |
|---|---|---|---|---|---|---|
| DET-001 | Detector | Test frame | Detection returned | Valid Detection object produced | Automated | Now |
| DET-002 | Filtering | Detection below threshold | Detection removed | Detection is excluded | Automated | Now |
| DET-003 | Filtering | Detection at/above threshold | Detection retained | Detection remains | Automated | Now |
| REN-001 | Rendering | Detection with bounding box | Box rendered | Bounding box appears at expected coordinates | Manual | Now |
| REN-002 | Rendering | Detection with class | Class label rendered | Label is visible and correct | Manual | Now |
| REN-003 | Rendering | Detection with confidence | Confidence displayed | Confidence value is visible | Manual | Now |
| REN-004 | Rendering | Tracked detection | Track ID displayed | Track ID is visible | Manual | Now |
| REN-005 | Rendering | Multiple detections | All detections rendered | Expected detections are visible | Manual | Final integration |
| REN-006 | Smoke detection | Smoke prediction | Smoke box rendered | Smoke class and box correspond to prediction | Manual | Final `.pt` |
| REN-007 | Fire detection | Fire prediction | Fire box rendered | Fire class and box correspond to prediction | Manual | Final `.pt` |

---

## 5.4 Tracking Tests

| ID | Component | Input | Expected Result | Pass/Fail Criteria | Type | Execution |
|---|---|---|---|---|---|---|
| TRK-001 | Tracker | Detection sequence | Track created | Detection receives track ID | Automated | Now |
| TRK-002 | Tracker | Consecutive overlapping detections | Track maintained | Same object maintains reasonable ID | Automated/Manual | Now |
| TRK-003 | Tracker | Different class | Class separation maintained | Different classes are not incorrectly matched | Automated | Now |
| TRK-004 | Tracker | Temporarily missing detection | Track persistence follows configuration | Track behavior respects missed-frame setting | Automated | Now |
| TRK-005 | Tracker | Difficult sequence | Temporal behavior reasonable | No obvious unstable ID behavior | Manual | Final `.pt` |

---

## 5.5 Statistics Tests

| ID | Component | Input | Expected Result | Pass/Fail Criteria | Type | Execution |
|---|---|---|---|---|---|---|
| STAT-001 | Statistics | Detection list | Detection count calculated | Count matches processed detections | Automated | Now |
| STAT-002 | Statistics | Smoke detections | Average smoke confidence calculated | Value matches input confidences | Automated | Now |
| STAT-003 | Statistics | Fire detections | Average fire confidence calculated | Value matches input confidences | Automated | Now |
| STAT-004 | Statistics | Detection list | Maximum confidence calculated | Maximum matches input | Automated | Now |
| STAT-005 | Statistics | Detection list | Minimum confidence calculated | Minimum matches input | Automated | Now |
| STAT-006 | Statistics | No detections | Empty/no-detection case handled | No crash or invalid calculation | Automated | Now |
| STAT-007 | Statistics | Completed inference | JSON generated | Valid statistics JSON exists | Automated | Now |
| STAT-008 | Statistics | Completed inference | Statistics correspond to run | Metadata and statistics are internally consistent | Automated | Now |

---

# 6. Model-Output QA

These tests require the final M2 `.pt` model.

| ID | Component | Input | Expected Result | Pass/Fail Criteria | Type | Execution |
|---|---|---|---|---|---|---|
| MODEL-001 | Classification | Smoke scene | Smoke classified as smoke | Prediction agrees with reference where applicable | Manual/Metric | Final `.pt` |
| MODEL-002 | Classification | Fire scene | Fire classified as fire | Prediction agrees with reference where applicable | Manual/Metric | Final `.pt` |
| MODEL-003 | Classification | Mixed smoke/fire scene | Classes separated correctly | No unjustified smoke/fire confusion | Manual/Metric | Final `.pt` |
| MODEL-004 | False positives | Negative/background scene | No unjustified detection | False-positive behavior evaluated | Manual/Metric | Final `.pt` |
| MODEL-005 | False negatives | Annotated smoke/fire | Detection produced where expected | Missed detections recorded | Manual/Metric | Final `.pt` |
| MODEL-006 | Small/distant smoke | Difficult smoke scene | Small smoke detected where expected | Missed small/distant smoke recorded | Manual | Final `.pt` |
| MODEL-007 | Fire | Difficult fire scene | Fire detected | Missed fire recorded | Manual | Final `.pt` |
| MODEL-008 | Bounding box | Annotated object | Localization is reasonable | Box sufficiently overlaps reference | Manual/Metric | Final `.pt` |
| MODEL-009 | Confidence | Predictions | Confidence behaves consistently | Confidence values are recorded and reviewed | Manual/Metric | Final `.pt` |
| MODEL-010 | Difficult scenes | Ambiguous scene | Behavior documented | Correct/incorrect behavior is recorded without modifying annotations | Manual | Final `.pt` |
| MODEL-011 | Temporal stability | Consecutive frames | Detection behavior is reasonably stable | Excessive flicker/ID instability recorded | Manual | Final `.pt` |

---

# 7. End-to-End Workflow

The complete system QA sequence is:

1. Upload a valid MP4.
2. Create a processing job.
3. Validate the uploaded video.
4. Start processing.
5. Run inference.
6. Generate annotated output video.
7. Generate detection statistics.
8. Mark the job as completed.
9. Retrieve the output video.
10. Retrieve statistics.
11. Display the result in the dashboard.

Failure paths must also be tested:

1. Invalid file upload
2. Missing file
3. Oversized file where a limit exists
4. Invalid job ID
5. Video validation failure
6. Processing failure
7. Inference failure
8. Output-generation failure
9. Statistics-generation failure

---

# 8. Current QA Findings

The following findings were observed during Phase 3 preparation.

## QA-001 — Phase 3 automated tests implemented

Initial pytest discovery produced no tests because the Phase 3 test suite had not yet been added.

M4 added the Phase 3 automated test suite covering detector behavior, filtering, tracking, statistics, and synthetic video processing.

Current result:

    14 passed

Status: Resolved

Owner: M4

---

## QA-002 — YOLO dependency is imported before detector selection

The inference entry point imports the YOLO detector module before selecting the detector type.

The YOLO detector imports the Ultralytics package.

As a result, the lightweight test environment cannot currently execute the inference CLI without the Ultralytics dependency, even when the `test` detector is intended to be used.

Status: Open

Owner: M1/M3

Impact:

The model-independent test path is available at the component level, but the complete CLI test path currently depends on the YOLO runtime package.

---

# 9. Test Execution Timing

## Can be tested now

- Detector interface
- TestDetector
- Filtering
- Tracker behavior
- Statistics
- Video validation
- Synthetic video processing
- Output-video structure
- Automated test framework
- Error-handling logic that already exists
- QA documentation

## Requires backend implementation

- API upload
- Job creation
- Job status
- Output retrieval
- Statistics retrieval
- Backend failure handling

## Requires final M2 `.pt`

- Smoke/fire classification quality
- False positives
- False negatives
- Smoke/fire confusion
- Small/distant smoke
- Fire detection quality
- Model confidence behavior
- Model bounding-box quality
- Difficult-scene evaluation
- Temporal model behavior

## Requires dashboard implementation

- Dashboard job display
- Dashboard processing state
- Dashboard completed state
- Dashboard output display
- Dashboard statistics display
- Dashboard failure display

---

# 10. QA Principles

1. Verified annotations are treated as the reference dataset for model-output QA where applicable.
2. Verified annotations must not be changed to make model results appear better.
3. Automated QA, manual visual QA, and model-performance evaluation remain separate.
4. M4 does not modify M2 training configuration.
5. M4 does not modify the verified dataset.
6. M4 does not implement the React frontend.
7. M4 prepares QA before the final M2 model is available.
8. Every failed test should record the observed behavior, expected behavior, impact, and owner.