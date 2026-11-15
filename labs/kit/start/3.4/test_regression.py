"""One regression test per defect: it fails on the defect and passes on your fix.

    uv run pytest test_regression.py

A regression test uses the smallest input that shows the problem, the one you found in the
"shrink" step. For a test that needs a file there is data/tiny.csv: two good rows of meter
M-0001. A test is a function whose name starts with test_ and that asserts what must hold.
"""

from pathlib import Path

from miqyas.anomalies import median  # noqa: F401
from miqyas.readings import load_readings  # noqa: F401

TINY = Path("data/tiny.csv")

# def test_defect_a_...():


# def test_defect_b_...():
