\# M3 Transition Frame Sampling



\## Purpose



Additional frames were extracted around visually important smoke/fire transition windows identified during the first-pass 10-second temporal review.



\## Sampling Method



Frames were sampled at approximately 1-second intervals within each transition window.



\## Transition Windows



\### video\_01.mp4



| Window | Event |

|---|---|

| 8s-12s | Smoke appearance |

| 28s-32s | Fire appearance |



\### video\_02.mp4



| Window | Event |

|---|---|

| 28s-32s | Smoke appearance |

| 38s-42s | Stronger smoke |

| 48s-52s | Fire appearance |

| 78s-82s | Smoke transition |

| 88s-92s | Fire + smoke transition |

| 98s-102s | Smoke transition |



\## Output



40 transition-review frames were extracted.



Output directory:



`data/frames/transition\_review/`



The generated JPG artifacts are excluded from Git.



The extraction logic is stored in:



`scripts/extract\_transition\_frames.py`



\## Reproducibility



Run:



`python scripts/extract\_transition\_frames.py`



The script reads the original videos from:



`data/raw/`



and regenerates the transition-review frames under:



`data/frames/transition\_review/`



\## Validation



\- video\_01: 10 transition frames

\- video\_02: 30 transition frames

\- Total: 40 transition-review frames

