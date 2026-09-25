# Agnidrishti — Team Handoff

## 1. Purpose

This document allows all four team members to work from the same project context and workflow without depending on one person's ChatGPT memory.

The repository and its documented decisions are the project's source of truth.

---

# 2. Team Allocation

| Member | Role | Hardware | Primary Responsibility |
|---|---|---|---|
| **M1 — You** | Dataset Lead + Integration | Normal laptop | Dataset architecture, integration, QC, decisions |
| **M2** | GPU/ML Pipeline | NVIDIA GPU laptop | Grounding DINO, GPU setup, later model training |
| **M3** | Video/Data Engineer | Normal laptop | Video inspection, frame extraction, data pipeline |
| **M4** | Annotation/QA Engineer | Normal laptop | Annotation, verification and label QA |

---

# 3. M1 — Dataset Lead + Integration

## Main Responsibility

M1 is responsible for making sure that the outputs from M2, M3 and M4 become one consistent dataset and codebase.

## Tasks

- Maintain repository structure.
- Maintain project documentation.
- Maintain the technical decision log.
- Define and approve the dataset split.
- Check for temporal/data leakage.
- Integrate M2/M3/M4 outputs.
- Maintain dataset statistics and manifests.
- Perform final Phase 1 quality control.
- Ensure organizer test videos never enter development/training.

## M1 Should NOT Become the Bottleneck

You do not need to manually perform every annotation or every preprocessing operation.

Your main job is integration and technical control.

---

# 4. M2 — GPU/ML Pipeline

## Hardware

NVIDIA GPU laptop.

## Main Responsibility

Use the GPU where it provides a real advantage.

## Phase 1 Tasks

1. Set up the CUDA/PyTorch environment.
2. Verify GPU availability.
3. Set up Grounding DINO if selected.
4. Test smoke/fire candidate detection.
5. Build a reproducible candidate-generation script.
6. Save candidate annotations in a format that M4 can review.
7. Record GPU memory use and inference behavior.

## Pipeline

```text
Frames from M3
       ↓
Grounding DINO
       ↓
Candidate boxes
       ↓
M4 human verification
       ↓
Final annotations
