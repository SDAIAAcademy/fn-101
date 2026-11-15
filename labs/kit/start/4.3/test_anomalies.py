"""Tests for the anomaly rule.

    uv run pytest test_anomalies.py

The rule, from the docstring of miqyas.anomalies.is_anomaly:

    True when value is more than factor times the median of history.
    With no history there is nothing to compare with: the answer is False.
    Exactly factor times the median is not an anomaly.

A test is a function whose name starts with test_. It arranges a small input, calls the
function, and asserts what must come back. One test is written; add at least five.
"""

from miqyas.anomalies import is_anomaly


def test_an_ordinary_reading_is_not_an_anomaly():
    assert is_anomaly(1.1, [1.0, 1.0, 1.0]) is False
