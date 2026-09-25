from scripts.inference.detector import Detection
from scripts.inference.tracker import IoUTracker


def make_detection(
    class_id=0,
    class_name="smoke",
    confidence=0.90,
    x1=10,
    y1=10,
    x2=100,
    y2=100,
):
    return Detection(
        class_id=class_id,
        class_name=class_name,
        confidence=confidence,
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
    )


def test_tracker_creates_track_for_detection():
    tracker = IoUTracker()

    detection = make_detection()

    tracks = tracker.update([detection])

    assert len(tracks) == 1
    assert tracks[0].track_id == 1
    assert tracks[0].detection == detection


def test_tracker_keeps_same_id_for_overlapping_detection():
    tracker = IoUTracker(iou_threshold=0.3)

    first_detection = make_detection(
        x1=10,
        y1=10,
        x2=100,
        y2=100,
    )

    second_detection = make_detection(
        x1=15,
        y1=15,
        x2=105,
        y2=105,
    )

    first_tracks = tracker.update([first_detection])
    second_tracks = tracker.update([second_detection])

    assert first_tracks[0].track_id == 1
    assert second_tracks[0].track_id == 1
    assert second_tracks[0].detection == second_detection


def test_tracker_does_not_match_different_classes():
    tracker = IoUTracker(iou_threshold=0.3)

    smoke = make_detection(
        class_id=0,
        class_name="smoke",
    )

    fire = make_detection(
        class_id=1,
        class_name="fire",
    )

    first_tracks = tracker.update([smoke])
    second_tracks = tracker.update([fire])

    assert first_tracks[0].track_id == 1

    track_ids = {track.track_id for track in second_tracks}

    assert 2 in track_ids


def test_tracker_creates_separate_tracks_for_non_overlapping_objects():
    tracker = IoUTracker(iou_threshold=0.3)

    detection_a = make_detection(
        x1=10,
        y1=10,
        x2=50,
        y2=50,
    )

    detection_b = make_detection(
        x1=200,
        y1=200,
        x2=250,
        y2=250,
    )

    tracks = tracker.update([detection_a, detection_b])

    assert len(tracks) == 2
    assert {track.track_id for track in tracks} == {1, 2}