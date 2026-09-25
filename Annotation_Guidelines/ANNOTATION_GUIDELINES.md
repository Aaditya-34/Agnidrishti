# Agnidrishti Annotation Guidelines

**Document:** Annotation Guidelines  
**Phase:** Phase 1  
**Status:** Draft v1  
**Scope:** Smoke and fire object detection  
**Classes:** 0 = smoke, 1 = fire

---

## 1. Purpose

This document defines the annotation policy for the Agnidrishti fire and smoke detection dataset.

The objective is to produce consistent, human-verified object-detection annotations suitable for later model training and evaluation.

M2/model-generated detections are candidate annotations only. They must never be treated as ground truth without human verification.

---

## 2. Class Definition

The dataset contains exactly two object classes.

| Class ID | Class |
|---|---|
| 0 | smoke |
| 1 | fire |

This mapping is fixed and must not be reversed or changed.

No additional object classes should be introduced during Phase 1.

---

# 3. General Annotation Principle

Annotations must be based on visible evidence in the image.

Annotators must not label an object merely because:

- a model predicted it,
- it appeared in a previous frame,
- it is expected to exist in the scene,
- another annotator labeled it,
- or it is likely to be present outside the visible region.

Model predictions are suggestions only.

The final label represents the human annotator's judgment of what is visibly supported by the frame.

---

# 4. Fire Annotation Policy

## 4.1 What counts as fire

Label visible flames as class `1`.

A fire annotation may include:

- isolated visible flames,
- a cluster of flames,
- flames emerging from an object,
- multiple visibly connected flame regions,
- partially occluded visible flames.

The annotation should cover the visible fire region rather than the entire object that is burning.

### Example

If flames are coming from a vehicle:

- label the visible flames,
- do not automatically box the entire vehicle.

---

## 4.2 Fire bounding boxes

The bounding box should tightly contain the visible fire region.

Avoid:

- excessive background,
- unrelated objects,
- large surrounding structures,
- arbitrary padding.

Small amounts of unavoidable background are acceptable when required to contain the visible target cleanly.

---

## 4.3 Multiple fire regions

If clearly separated fire regions are visually distinct, annotate them separately.

Do not create many tiny boxes for fragments that are visually part of one continuous flame region.

---

# 5. Smoke Annotation Policy

Smoke is more difficult to annotate than fire because it is often diffuse, transparent, irregular, and partially blended with the background.

The smoke policy must therefore prioritize **identifiable visual evidence** over aggressive labeling.

---

## 5.1 What counts as smoke

Label smoke when there is reasonably identifiable visible smoke structure.

Useful visual evidence may include:

- persistent plume-like structure,
- characteristic wispy or billowing shape,
- visible smoke emerging from a source,
- contrast between smoke and the background,
- dense smoke clouds,
- clearly visible smoke surrounding a fire.

---

## 5.2 Thin smoke

Thin smoke should be labeled only when the smoke is sufficiently distinguishable from the background.

Do not create a box around an area merely because it could possibly contain smoke.

If the annotator cannot confidently identify the visible smoke boundary:

`needs_review`

should be used when supported by the annotation workflow.

---

## 5.3 Dense smoke

Dense smoke should be annotated when the smoke region is visually identifiable.

The box should cover the visible smoke mass rather than only the darkest central portion.

Avoid including large amounts of unrelated background.

---

## 5.4 Irregular smoke

Smoke does not normally have a rectangular shape.

Bounding boxes are still required because this is an object-detection dataset.

The box should be the smallest reasonable rectangle that contains the identifiable smoke region.

Do not attempt to follow every small contour or wispy edge.

---

## 5.5 Smoke mixed with background

When smoke gradually blends into the background:

- annotate the clearly identifiable portion,
- do not extend the box arbitrarily into visually unsupported regions,
- mark for review if the boundary cannot be reasonably determined.

---

## 5.6 Smoke behind structures

If smoke is partially hidden by:

- buildings,
- trees,
- vehicles,
- poles,
- equipment,
- or other structures,

annotate only the visible smoke.

Do not infer the hidden portion.

---

## 5.7 Partially visible smoke

A partially visible smoke region should still be annotated when the visible portion is sufficiently identifiable.

The bounding box should correspond to the visible evidence.

Do not reconstruct or extrapolate the hidden smoke.

---

# 6. Ambiguous Smoke Cases

An image should be considered ambiguous when the annotator cannot reasonably distinguish smoke from another visual phenomenon.

Potential examples include:

- fog,
- dust,
- steam,
- clouds,
- atmospheric haze,
- compression artifacts,
- glare,
- exhaust,
- background objects with smoke-like appearance.

Do not force an annotation when the evidence is insufficient.

Use the review mechanism where available.

Recommended review category:

`needs_review`

---

# 7. Smoke vs Steam / Dust / Fog

Do not automatically classify every white or gray plume as smoke.

The annotator should consider visible context.

Examples:

- A clearly visible flame with an associated plume may provide supporting context.
- A white cloud with no identifiable fire context should not automatically be labeled smoke.
- Vehicle exhaust should not automatically be labeled smoke.
- Steam should not automatically be labeled smoke.
- Dust clouds should not automatically be labeled smoke.

When the distinction cannot reasonably be made from the frame, escalate for review rather than guessing.

---

# 8. Fire + Smoke in the Same Image

An image may contain both classes.

Example:

```text
class 0 → smoke
class 1 → fire