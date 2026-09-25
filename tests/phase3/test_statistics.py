from scripts.inference.detector import Detection
from scripts.inference.statistics import ConfidenceStatistics


def make_detection(class_id, class_name, confidence):
    return Detection(
        class_id=class_id,
        class_name=class_name,
        confidence=confidence,
        x1=10,
        y1=10,
        x2=100,
        y2=100,
    )


def test_statistics_for_smoke():
    statistics = ConfidenceStatistics()

    detections = [
        make_detection(0, "smoke", 0.80),
        make_detection(0, "smoke", 0.90),
    ]

    statistics.update(detections)

    result = statistics.summary()

    assert result["smoke"]["detections"] == 2
    assert result["smoke"]["average_confidence"] == 0.85
    assert result["smoke"]["maximum_confidence"] == 0.90
    assert result["smoke"]["minimum_confidence"] == 0.80


def test_statistics_for_fire():
    statistics = ConfidenceStatistics()

    detections = [
        make_detection(1, "fire", 0.70),
        make_detection(1, "fire", 0.90),
    ]

    statistics.update(detections)

    result = statistics.summary()

    assert result["fire"]["detections"] == 2
    assert result["fire"]["average_confidence"] == 0.80
    assert result["fire"]["maximum_confidence"] == 0.90
    assert result["fire"]["minimum_confidence"] == 0.70


def test_statistics_separates_classes():
    statistics = ConfidenceStatistics()

    detections = [
        make_detection(0, "smoke", 0.80),
        make_detection(1, "fire", 0.90),
    ]

    statistics.update(detections)

    result = statistics.summary()

    assert result["smoke"]["detections"] == 1
    assert result["fire"]["detections"] == 1


def test_statistics_handles_no_detections():
    statistics = ConfidenceStatistics()

    result = statistics.summary()

    assert result == {}