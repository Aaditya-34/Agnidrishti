# Agnidrishti

AI-powered smoke and fire detection and visualization system for the hackathon.

## Project Identity

- **Project name:** Agnidrishti
- **Target problem:** Smoke and fire detection in video
- **Camera:** Fixed angle
- **Target classes:**
  - `0 = smoke`
  - `1 = fire`

## Team

| Member | Role | Hardware |
|---|---|---|
| M1 | Dataset Lead + Integration | Normal laptop |
| M2 | GPU/ML Pipeline | NVIDIA GPU laptop |
| M3 | Video/Data Engineer | Normal laptop |
| M4 | Annotation/QA Engineer | Normal laptop |

## Current Raw Data

The project currently has two source MP4 videos:

- Video 1: approximately 274 MB / approximately 3 minutes
- Video 2: approximately 65 MB / approximately 2 minutes

Exact video metadata such as resolution, FPS, frame count, codec and bitrate will be recorded after inspection.

## Phase 1 Goal

Create a reproducible, validated, training-ready object-detection dataset for smoke and fire.

High-level pipeline:

```text
Raw Videos
    ↓
Video Inspection
    ↓
Smart Frame / Event Sampling
    ↓
Near-Duplicate Reduction
    ↓
Annotation Assistance
    ↓
Human Verification
    ↓
Dataset QA
    ↓
Video/Temporal-Aware Split
    ↓
YOLO Training Dataset
