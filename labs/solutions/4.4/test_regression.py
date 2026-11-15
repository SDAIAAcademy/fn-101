"""The regression test of defect C: it fails on the defect and passes on the fix."""

from datetime import date

from miqyas.anomalies import Anomaly
from miqyas.readings import Meter
from miqyas.report import anomalies_by_district

METERS = {"M-0001": Meter("M-0001", "Al-Rabwa", "residential"),
          "M-0002": Meter("M-0002", "Al-Yasmin", "residential")}


def test_defect_c_an_anomaly_is_listed_in_its_own_district_only():
    anomaly = Anomaly("M-0001", date(2026, 9, 1), 9.0, 1.0)
    groups = anomalies_by_district([anomaly], METERS)
    assert groups == {"Al-Rabwa": [anomaly], "Al-Yasmin": []}
    assert groups["Al-Rabwa"] is not groups["Al-Yasmin"]
