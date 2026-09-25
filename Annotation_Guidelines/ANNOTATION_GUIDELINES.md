# Agnidrishti — Annotation Guidelines

## 1. Purpose

This document defines the rules for creating and verifying bounding-box annotations for the Agnidrishti dataset.

The dataset contains two detection classes:

- smoke
- fire

The objective is to maintain consistent annotations across all team members.

## 2. Class Mapping

| Class ID | Class Name |
|---|---|
| 0 | smoke |
| 1 | fire |

This mapping must not be changed after verified annotations are created.

## 3. General Annotation Rules

For every annotation:

1. Annotate only visible target regions.
2. Use bounding boxes.
3. Keep the bounding box around the target as accurately as possible.
4. Avoid including unnecessary background.
5. Do not create an annotation when there is insufficient evidence that the target is present.
6. Apply the same rule consistently across similar frames.

## 4. Smoke Annotation

Smoke can have diffuse and irregular boundaries.

Annotators should:

- include the visible smoke region
- avoid large amounts of unrelated background
- avoid treating fog, clouds, dust, steam, or gray regions as smoke without sufficient evidence
- maintain consistent annotation behavior across similar frames

When the boundary of smoke is unclear, annotate the region supported by visible evidence rather than inventing an exact boundary.

## 5. Fire Annotation

Annotators should:

- include the visible fire region
- cover the visible flame area
- avoid unrelated background
- avoid bright lights, reflections, or other bright objects
- maintain consistent bounding boxes across similar frames

## 6. Multiple Objects

If multiple separate smoke or fire regions are visible, annotate each distinct region separately when each region can reasonably be localized.

Do not create multiple boxes for the same continuous region without a clear reason.

## 7. Partial Visibility

When only part of a smoke or fire region is visible:

- annotate the visible portion
- do not assume the hidden portion
- do not extend the box into areas where the target cannot be supported visually

## 8. Small Objects

Small visible smoke or fire regions should not automatically be discarded.

If the target is sufficiently identifiable, annotate it.

Difficult small-object examples should be flagged for QA.

## 9. Ambiguous Cases

Examples of potentially confusing regions include:

- fog
- clouds
- dust
- steam
- gray background
- reflections
- bright lights
- compression artifacts

These should not automatically be classified as smoke or fire.

If an example is difficult to classify, flag it for QA review.

## 10. Candidate Annotations

Automated annotation tools may be used to generate candidate annotations.

Candidate annotations are not considered ground truth.

The workflow is:

```text
Candidate Annotation
        ↓
Human Review
        ↓
Correction
        ↓
Accepted / Rejected
        ↓
Verified Annotation