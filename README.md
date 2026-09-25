# Agnidrishti

AI-based video fire and smoke detection system.

## 1. Project Overview

Agnidrishti is a computer-vision system designed to detect smoke and fire in video and provide localized detections with confidence scores.

The system is being developed as part of the KSIT ElectroHack 4.0 challenge.

## 2. Detection Classes

| Class ID | Class Name |
|---|---|
| 0 | smoke |
| 1 | fire |

## 3. Main Pipeline

```text
Input Video
    ↓
Video Processing
    ↓
Frame Sampling
    ↓
Object Detection
    ↓
Smoke / Fire Detection
    ↓
Bounding Boxes + Confidence
    ↓
Temporal Stabilization / Tracking
    ↓
Processed Video
    ↓
Detection Statistics