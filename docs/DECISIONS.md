# Agnidrishti — Technical Decisions

## 1. Purpose

This document records important technical decisions made during the development of Agnidrishti.

The purpose is to distinguish:

- confirmed decisions
- proposed approaches
- open decisions

This prevents experimental ideas from being treated as final requirements.

## 2. Confirmed Decisions

### D001 — Project Name

**Decision:** The project name is Agnidrishti.

**Status:** Confirmed

---

### D002 — Camera Scenario

**Decision:** The current development videos use a fixed-camera setup.

**Status:** Confirmed

---

### D003 — Detection Classes

**Decision:**

| Class ID | Class Name |
|---|---|
| 0 | smoke |
| 1 | fire |

**Status:** Confirmed

---

### D004 — Human Verification

**Decision:** Automated candidate annotations must be reviewed by humans before entering the verified dataset.

**Status:** Confirmed

---

### D005 — Organizer Test Data Separation

**Decision:** Organizer-provided unseen test videos must not be used for training, validation, annotation generation, pseudo-labeling, or model tuning.

**Status:** Confirmed

---

### D006 — Temporal Leakage Prevention

**Decision:** Train/validation splitting must account for temporal correlation between frames.

**Status:** Confirmed

## 3. Proposed Technical Approaches

The following are current engineering proposals and may change after experiments.

### D007 — Initial Detector

**Proposal:** Begin experiments with a pretrained Ultralytics YOLO model.

The exact model variant will be selected after benchmarking.

**Status:** Proposed

---

### D008 — Model Benchmarking

**Proposal:** Compare suitable lightweight and medium-sized YOLO variants rather than assuming a single model is optimal.

Evaluation should consider:

- precision
- recall
- mAP
- false positives
- false negatives
- inference speed
- resource usage

**Status:** Proposed

---

### D009 — Candidate Annotation Assistance

**Proposal:** Evaluate Grounding DINO or a similar foundation-model-based method for generating candidate annotations.

These outputs will remain candidates until human verification.

**Status:** Proposed

---

### D010 — Lightweight Tracking

**Proposal:** Evaluate lightweight object tracking for video inference if it improves temporal consistency.

**Status:** Proposed

---

### D011 — Temporal Stabilization

**Proposal:** Evaluate temporal confidence smoothing or similar methods to reduce unstable frame-to-frame detections.

**Status:** Proposed

---

### D012 — Backend

**Proposal:** Use FastAPI for the backend API.

**Status:** Proposed

---

### D013 — Frontend

**Proposal:** Use React or a compatible React-based framework for the dashboard.

**Status:** Proposed

---

### D014 — Inference Optimization

**Proposal:** Use PyTorch/CUDA as the initial inference environment.

Evaluate TensorRT later if inference optimization is required.

**Status:** Proposed

## 4. Open Decisions

### D015 — Frame Sampling Rate

The final sampling rate has not yet been selected.

**Status:** Open

**Owner:** M3

---

### D016 — Event-Based Sampling

Determine whether event-aware sampling provides useful dataset diversity compared with fixed-rate sampling.

**Status:** Open

**Owner:** M3

---

### D017 — Annotation Tool Workflow

Determine the final annotation workflow and tool usage after initial testing.

**Status:** Open

**Owner:** M4

---

### D018 — Candidate Annotation Configuration

Determine the configuration and workflow for any foundation-model-based candidate annotation system.

**Status:** Open

**Owner:** M2

---

### D019 — Final Dataset Size

Determine the required number of training and validation images after sampling and annotation analysis.

**Status:** Open

**Owner:** M1 + M3 + M4

---

### D020 — Train / Validation Split

Determine the final split strategy after understanding the source videos and temporal groups.

**Status:** Open

**Owner:** M1 + M3

---

### D021 — Region of Interest

Determine whether a fixed region of interest is useful for the current camera setup.

**Status:** Open

**Owner:** M1 + M3

---

### D022 — Final Detector

Select the final detector after controlled experiments.

**Status:** Open

**Owner:** M2

---

### D023 — Final Tracker

Determine whether tracking is required and which approach should be used.

**Status:** Open

**Owner:** M2

---

### D024 — Detection Confidence Threshold

Determine the confidence threshold using validation results and error analysis.

**Status:** Open

**Owner:** M2 + M1

---

### D025 — SAHI

Determine whether sliced inference is required for small-object detection.

SAHI should only be introduced if experiments demonstrate a meaningful small-object limitation.

**Status:** Open

**Owner:** M2

## 5. Decision Change Process

When an important technical decision changes:

1. Update this document.
2. Change the decision status.
3. Record the reason.
4. Record supporting experiment results when available.
5. Inform affected team members.
6. Update other project documents if necessary.

## 6. Decision Status Definitions

### Confirmed

The team has agreed to use this approach.

### Proposed

The approach is currently being considered or tested.

### Open

The decision has not yet been finalized.

## 7. Important Principle

A proposed technical approach must not be presented as a final project requirement until it has been confirmed by the team or supported by the required experiment.