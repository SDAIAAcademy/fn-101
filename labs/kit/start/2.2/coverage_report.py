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
    raise NotImplementedError("step 1: two sets and one operator")


def unknown_meters(readings: list[Row], meters: list[Row]) -> list[str]:
    """The meter ids that appear in the readings and are not in the registry, sorted."""
    raise NotImplementedError("step 2: the same two sets, the other way round")


def repeated_keys(readings: list[Row]) -> set[tuple[str, str]]:
    """Every (meter_id, date) pair that appears more than once in the readings."""
    raise NotImplementedError("step 3: a set of the pairs seen so far")


if __name__ == "__main__":
    readings = load("data/readings_2026_09.csv")
    meters = load("data/meters.csv")
    silent = silent_meters(readings, meters)
    unknown = unknown_meters(readings, meters)
    print(len(silent), "meters sent nothing:", ", ".join(silent))
    print(len(unknown), "unknown ids in the readings:", ", ".join(unknown))
    print(len(repeated_keys(readings)), "(meter, date) pairs appear more than once")
