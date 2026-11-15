"""Load and validate daily meter readings.

A row is either accepted as a Reading or rejected with a reason code. Nothing is dropped
silently: accepted rows plus rejections always equals the data rows of the file.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path

MAX_DAILY_M3 = 200.0


@dataclass(frozen=True)
class Meter:
    meter_id: str
    district: str
    kind: str


@dataclass(frozen=True)
class Reading:
    meter_id: str
    day: date
    m3: float


@dataclass(frozen=True)
class Rejection:
    line_no: int
    reason: str
    detail: str


class RejectedRow(Exception):
    """A row that cannot be accepted; reason is a short code, detail is for a person."""

    def __init__(self, reason: str, detail: str) -> None:
        super().__init__(f"{reason}: {detail}")
        self.reason = reason
        self.detail = detail


def parse_value(text: str) -> float:
    """Turn the consumption cell into cubic metres, or say why not.

    >>> parse_value(" 0.750 ")
    0.75
    >>> parse_value("12")
    12.0
    """
    text = text.strip()
    if text == "":
        raise RejectedRow("MISSING_VALUE", "consumption_m3 is empty")
    try:
        value = float(text)
    except ValueError:
        raise RejectedRow("NOT_A_NUMBER", f"consumption_m3 is {text!r}") from None
    if not 0.0 <= value <= MAX_DAILY_M3:
        raise RejectedRow("OUT_OF_RANGE", f"{value} is outside 0 to {MAX_DAILY_M3}")
    return value


def parse_row(row: dict[str, str], known: set[str]) -> Reading:
    """Validate one row of the readings file against the meter registry."""
    m3 = parse_value(row["consumption_m3"])
    try:
        day = date.fromisoformat(row["date"])
    except ValueError:
        raise RejectedRow("BAD_DATE", f"date is {row['date']!r}") from None
    meter_id = row["meter_id"]
    if meter_id not in known:
        raise RejectedRow("UNKNOWN_METER", f"{meter_id} is not in the registry")
    return Reading(meter_id, day, m3)


def load_meters(path: Path) -> dict[str, Meter]:
    """The meter registry, by meter id."""
    with open(path, encoding="utf-8", newline="") as file:
        return {row["meter_id"]: Meter(row["meter_id"], row["district"], row["kind"])
                for row in csv.DictReader(file)}


def load_readings(
    path: Path,
    known: set[str],
    seen: set[tuple[str, date]] | None = None,
) -> tuple[list[Reading], list[Rejection]]:
    """Read a readings file: the accepted readings and one rejection per refused row.

    seen holds the (meter, day) pairs already accepted; pass the same set when a month
    arrives in several files, so that a repeat in a later file is a DUPLICATE too.
    """
    if seen is None:
        seen = set()
    accepted: list[Reading] = []
    rejected: list[Rejection] = []
    with open(path, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                reading = parse_row(row, known)
                key = (reading.meter_id, reading.day)
                if key in seen:
                    raise RejectedRow("DUPLICATE", f"{reading.meter_id} already has {reading.day}")
            except RejectedRow as problem:
                rejected.append(Rejection(reader.line_num, problem.reason, problem.detail))
                continue
            seen.add(key)
            accepted.append(reading)
    return accepted, rejected
