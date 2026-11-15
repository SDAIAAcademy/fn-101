"""The anomaly rule: a reading far above what the meter usually shows."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from miqyas.readings import Reading


@dataclass(frozen=True)
class Anomaly:
    meter_id: str
    day: date
    m3: float
    median: float


def median(values: list[float]) -> float:
    """The middle value; the mean of the two middle values for an even count."""
    if not values:
        raise ValueError("median of no values")
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def is_anomaly(value: float, history: list[float], factor: float = 3.0) -> bool:
    """True when value is more than factor times the median of history.

    With no history there is nothing to compare with: the answer is False.
    Exactly factor times the median is not an anomaly.
    """
    if not history:
        return False
    return value > factor * median(history)


def find_anomalies(readings: list[Reading], factor: float = 3.0) -> list[Anomaly]:
    """Every reading that is an anomaly against its own meter's month, in a fixed order."""
    by_meter: dict[str, list[float]] = {}
    for reading in readings:
        by_meter.setdefault(reading.meter_id, []).append(reading.m3)
    found = [
        Anomaly(r.meter_id, r.day, r.m3, median(by_meter[r.meter_id]))
        for r in readings
        if is_anomaly(r.m3, by_meter[r.meter_id], factor)
    ]
    return sorted(found, key=lambda a: (a.meter_id, a.day))
