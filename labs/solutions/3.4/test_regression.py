"""One regression test per defect: it fails on the defect and passes on the fix."""

from pathlib import Path

from miqyas.anomalies import median
from miqyas.readings import load_readings

TINY = Path("data/tiny.csv")


def test_defect_a_a_second_call_starts_with_nothing_seen():
    first, _ = load_readings(TINY, {"M-0001"})
    second, rejected = load_readings(TINY, {"M-0001"})
    assert len(first) == 2
    assert len(second) == 2, f"the second call rejected {[r.reason for r in rejected]}"


def test_defect_b_median_does_not_depend_on_the_order():
    assert median([3.0, 1.0, 2.0]) == 2.0
    assert median([4.0, 1.0, 3.0, 2.0]) == 2.5
