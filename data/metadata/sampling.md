# M3 Frame Sampling

## Sampling Method

Representative frames were extracted from both source videos using a fixed 2-second sampling interval.

## Sampling Results

| Video | Duration | FPS | Sample Interval | Frames Extracted |
|---|---:|---:|---:|---:|
| video_01.mp4 | 190.600 s | 30.000 | 2 s | 96 |
| video_02.mp4 | 135.562 s | 29.883 | 2 s | 68 |
| Total | 326.162 s | - | 2 s | 164 |

## Rationale

A 10-second temporal preview was first used to identify major visual/event segments.

Based on that inspection, a 2-second sampling interval was selected for the first-pass representative frame set. This is not the final dataset sampling strategy and will be reviewed after annotation and QA.

## Frame Naming

Frames use the following naming format:

`<video_id>_t<timestamp>.jpg`

Examples:

- `video_01_t00010.000.jpg`
- `video_02_t00010.039.jpg`

The timestamp represents the actual sampled frame timestamp derived from the source video's frame position and FPS.

## Output

The sampled frames are stored locally under:

- `data/frames/video_01/`
- `data/frames/video_02/`

The frame manifest is stored at:

- `data/manifests/frames.csv`

The extracted frame files are excluded from Git because they are generated dataset artifacts.

## Phase 1 Status

- No model training was performed.
- No model inference was performed.
- Source video resolution was preserved during extraction.
- This is a first-pass representative frame set and may be refined during annotation/QA.
