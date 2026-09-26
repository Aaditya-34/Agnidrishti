# M3 Temporal / Event Segmentation

## video_01.mp4

| Start | End | Observable Event | Notes |
|---|---|---|---|
| 00s | 10s | Idle/background | No visible smoke or fire |
| 10s | 30s | Smoke | Smoke becomes visible and persists |
| 30s | 190.6s | Fire | Visible fire continues for the remainder of the video |

## video_02.mp4

| Start | End | Observable Event | Notes |
|---|---|---|---|
| 00s | 30s | Person/background | Person and background scene remain largely unchanged |
| 30s | 40s | Light smoke | Small amount of smoke becomes visible |
| 40s | 50s | Smoke | Smoke becomes more visible |
| 50s | 60s | Fire | Fire becomes visible |
| 60s | 80s | Fire + person | Fire remains visible with person in scene |
| 80s | 90s | Smoke | Smoke visible; fire is not clearly visible in preview |
| 90s | 100s | Fire + smoke | Both fire and smoke are visible |
| 100s | 135.6s | Smoke | Smoke remains visible through the end of the video |

## Analysis Method

- Preview interval: 10 seconds
- Analysis based on representative temporal preview frames
- Events describe observable visual content
- No ML inference was used
- Segments are first-pass temporal observations and may be refined during denser sampling
