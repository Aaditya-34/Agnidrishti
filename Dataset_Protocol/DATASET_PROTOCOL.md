# Agnidrishti — Dataset Protocol

## 1. Purpose

This document defines how the Agnidrishti dataset will be prepared for fire and smoke detection.

It covers:

- source video handling
- frame extraction
- frame sampling
- duplicate reduction
- annotation
- annotation verification
- quality checks
- train/validation splitting
- dataset structure
- dataset versioning

## 2. Dataset Classes

| Class ID | Class Name |
|---|---|
| 0 | smoke |
| 1 | fire |

These class IDs must remain consistent throughout the project.

## 3. Source Videos

All source videos used for dataset preparation must be recorded in a video inventory.

The inventory should contain:

| Field | Description |
|---|---|
| Video ID | Unique identifier |
| Filename | Original video filename |
| Duration | Video duration |
| FPS | Frames per second |
| Width | Video width |
| Height | Video height |
| Source | Source of the video |
| Notes | Relevant observations |

Exact values should be obtained during video inspection rather than estimated.

## 4. Organizer Test Videos

Organizer-provided unseen test videos must remain separate from the development dataset.

They must not be used for:

- training
- validation
- candidate annotation generation
- pseudo-labeling
- model tuning
- threshold selection

They should only be used for final evaluation according to the challenge requirements.

## 5. Frame Sampling

Frames should not simply be extracted from every video frame.

The sampling process should consider:

- temporal redundancy
- changes in smoke
- changes in fire
- camera stability
- scene changes
- difficult cases
- rare events

The final sampling strategy will be decided after M3 completes the video inspection.

The selected strategy must be documented and reproducible.

## 6. Near-Duplicate Reduction

Continuous video footage can contain many visually similar frames.

Near-duplicate analysis should be used to reduce unnecessary repetition while preserving meaningful visual variation.

Important or difficult frames should not be removed only because they are similar to nearby frames.

## 7. Annotation Workflow

The annotation workflow is:

```text
Sampled Frame
    ↓
Candidate Annotation
    ↓
Human Verification
    ↓
Correction / Addition / Removal
    ↓
Verified Annotation
    ↓
Annotation QA