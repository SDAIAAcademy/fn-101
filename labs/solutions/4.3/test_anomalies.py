"""Tests for the anomaly rule: an ordinary case and five that pin the rule down."""

from miqyas.anomalies import is_anomaly


def test_an_ordinary_reading_is_not_an_anomaly():
    assert is_anomaly(1.1, [1.0, 1.0, 1.0]) is False


def test_a_reading_far_above_the_median_is_an_anomaly():
    assert is_anomaly(5.0, [1.0, 1.0, 1.0]) is True


def test_exactly_three_times_the_median_is_not_an_anomaly():
    assert is_anomaly(3.0, [1.0, 1.0, 1.0]) is False


def test_just_above_three_times_the_median_is_an_anomaly():
    assert is_anomaly(3.001, [1.0, 1.0, 1.0]) is True


def test_no_history_is_never_an_anomaly():
    assert is_anomaly(100.0, []) is False


def test_the_median_is_used_and_one_extreme_day_does_not_move_it():
    history = [1.0, 1.0, 1.0, 1.0, 10.0]       # median 1.0, mean 2.8
    assert is_anomaly(3.5, history) is True


def test_the_factor_argument_changes_the_threshold():
    assert is_anomaly(2.5, [1.0, 1.0, 1.0], factor=2.0) is True
    assert is_anomaly(2.5, [1.0, 1.0, 1.0], factor=3.0) is False
