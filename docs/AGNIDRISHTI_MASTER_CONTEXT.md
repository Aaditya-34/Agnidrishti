# Agnidrishti — Master Project Context

## 1. Project Identity

Project Name: Agnidrishti

Project Type: AI-based video fire and smoke detection system

Primary Detection Classes:

| Class ID | Class Name |
|---|---|
| 0 | smoke |
| 1 | fire |

The system is intended to process video and detect smoke and fire using object detection.

## 2. Challenge Objective

The project must address three major areas:

1. Dataset preparation
2. Model development and evaluation
3. Working dashboard/system for video processing

The final system should be able to process a video and provide detection results including:

- detected class
- bounding box
- confidence score
- processed output video
- average confidence for each detected class

## 3. High-Level System Pipeline

```text
Raw Video
    ↓
Video Inspection
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
Train / Validation Dataset
    ↓
Model Training
    ↓
Model Evaluation
    ↓
Video Inference
    ↓
Temporal Stabilization / Tracking
    ↓
Processed Video
    ↓
Detection Statistics
    ↓
Dashboard