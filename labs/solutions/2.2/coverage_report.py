"""Which meters sent nothing, and which readings belong to no known meter?

Readings are the rows of data/readings_2026_09.csv, as they arrived (bad rows included).
Meters are the rows of data/meters.csv, the registry.
"""

import csv

Row = dict[str, str]


def load(path: str) -> list[Row]:
    """Read a CSV file; return one dictionary of strings per data row."""
    with open(path, encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def silent_meters(readings: list[Row], meters: list[Row]) -> list[str]:
    """The ids of the registry's meters that have no row in the readings, sorted."""
    registered = {meter["meter_id"] for meter in meters}
    reporting = {reading["meter_id"] for reading in readings}
    return sorted(registered - reporting)


def unknown_meters(readings: list[Row], meters: list[Row]) -> list[str]:
    """The meter ids that appear in the readings and are not in the registry, sorted."""
    registered = {meter["meter_id"] for meter in meters}
    reporting = {reading["meter_id"] for reading in readings}
    return sorted(reporting - registered)


def repeated_keys(readings: list[Row]) -> set[tuple[str, str]]:
    """Every (meter_id, date) pair that appears more than once in the readings."""
    seen: set[tuple[str, str]] = set()
    repeated: set[tuple[str, str]] = set()
    for reading in readings:
        key = (reading["meter_id"], reading["date"])
        if key in seen:
            repeated.add(key)
        seen.add(key)
    return repeated


if __name__ == "__main__":
    readings = load("data/readings_2026_09.csv")
    meters = load("data/meters.csv")
    silent = silent_meters(readings, meters)
    unknown = unknown_meters(readings, meters)
    print(len(silent), "meters sent nothing:", ", ".join(silent))
    print(len(unknown), "unknown ids in the readings:", ", ".join(unknown))
    print(len(repeated_keys(readings)), "(meter, date) pairs appear more than once")
