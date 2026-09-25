# M3 Source Video Metadata

Inspection date: 2026-09-25

## video_01.mp4

- Duration: 190.600 seconds (~3 minutes 10.6 seconds)
- Resolution: 1080 x 1920
- Orientation: Portrait
- FPS: 30.000
- Frame count: 5718
- Codec: H.264
- Inspection method: OpenCV

## video_02.mp4

- Duration: 135.562 seconds (~2 minutes 15.6 seconds)
- Resolution: 1920 x 1080
- Orientation: Landscape
- FPS: 29.883
- Frame count: 4051
- Codec: H.264
- Inspection method: OpenCV

## Combined Source Summary

- Number of source videos: 2
- Combined duration: 326.162 seconds (~5 minutes 26.2 seconds)
- Combined source frame count: 9769
- Video codecs: H.264
- Source orientations:
  - video_01.mp4: Portrait
  - video_02.mp4: Landscape

## Phase 1 Notes

- Both MP4 files were successfully opened and inspected using OpenCV.
- Raw source videos are stored locally under `data/raw/`.
- Raw source videos are excluded from Git via `.gitignore`.
- No model training was performed.
- No model inference was performed.