# Agnidrishti — Phase 1 Plan

## 1. Purpose

Phase 1 establishes the foundation required before serious model training.

The goal is to understand the source videos, establish the dataset strategy, define annotation rules, configure the development environment, and prepare the initial dataset pipeline.

## 2. Phase 1 Objectives

1. Inspect all available source videos.
2. Record video metadata.
3. Understand temporal and visual characteristics.
4. Define a frame-sampling strategy.
5. Reduce near-duplicate frames.
6. Establish annotation rules for smoke and fire.
7. Generate candidate annotations where useful.
8. Perform human verification.
9. Perform annotation quality checks.
10. Establish train/validation splitting rules without temporal leakage.
11. Prepare the dataset structure for YOLO training.
12. Record important decisions and assumptions.

## 3. Dataset Classes

| Class ID | Class Name |
|---|---|
| 0 | smoke |
| 1 | fire |

These class IDs must remain consistent across annotation, training, validation, inference, and reporting.

## 4. Team Responsibilities

### M1 — Integration / Dataset Lead

- Maintain project structure.
- Maintain master documentation.
- Coordinate the dataset pipeline.
- Integrate outputs from M2, M3, and M4.
- Track decisions and unresolved issues.
- Maintain Git branches and integration.
- Ensure organizer test data remains separated.

### M2 — GPU / ML Pipeline

- Configure NVIDIA, CUDA, and PyTorch environment.
- Evaluate candidate annotation assistance tools.
- Test candidate-generation workflows.
- Record GPU and inference information.
- Prepare the training environment.
- Avoid premature large-scale training.

### M3 — Video / Data Engineering

- Inspect source videos.
- Extract video metadata.
- Analyze temporal structure.
- Design frame sampling.
- Identify redundant frames.
- Identify difficult visual conditions.
- Produce frame manifests.
- Prevent temporal leakage.

### M4 — Annotation / QA

- Maintain annotation rules.
- Perform human verification.
- Correct candidate annotations.
- Add missing annotations.
- Remove invalid annotations.
- Validate YOLO labels.
- Produce annotation statistics.
- Document difficult cases.

## 5. Phase 1 Workflow

Raw Videos  
↓  
Video Inspection  
↓  
Metadata Collection  
↓  
Temporal / Event Analysis  
↓  
Frame Sampling  
↓  
Near-Duplicate Reduction  
↓  
Candidate Annotation  
↓  
Human Verification  
↓  
Annotation QA  
↓  
Dataset Split  
↓  
YOLO Dataset

## 6. Dataset Principles

### 6.1 Avoid Random Frame Leakage

Frames from the same continuous video segment should not be randomly distributed between training and validation.

Highly similar adjacent frames can otherwise appear in both sets and produce misleading validation results.

### 6.2 Preserve Difficult Cases

The dataset should preserve difficult examples such as:

- weak smoke
- dense smoke
- partially visible fire
- small fire regions
- low-contrast smoke
- occlusion
- changing illumination
- visually ambiguous regions
- smoke-like non-fire regions

### 6.3 Human Verification

Candidate annotations are not automatically ground truth.

Final training annotations require human verification.

## 7. Phase 1 Deliverables

The expected dataset structure is:

```text
data/
├── frames/
├── annotations/
│   ├── candidates/
│   └── verified/
└── dataset/
    ├── images/
    │   ├── train/
    │   └── val/
    └── labels/
        ├── train/
        └── val/