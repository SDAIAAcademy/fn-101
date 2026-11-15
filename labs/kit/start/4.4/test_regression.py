"""The regression test of defect C: it fails on the defect and passes on your fix.

    uv run pytest test_regression.py

Build the smallest case by hand: two meters in two districts and one anomaly.
"""

from datetime import date  # noqa: F401

from miqyas.anomalies import Anomaly  # noqa: F401
from miqyas.readings import Meter  # noqa: F401
from miqyas.report import anomalies_by_district  # noqa: F401

# def test_defect_c_...():
