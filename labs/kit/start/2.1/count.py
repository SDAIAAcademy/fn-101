"""Count readings per meter and per district.

A reading is one row of data/readings_clean.csv: meter_id, date, consumption_m3.
A meter is one row of data/meters.csv: meter_id, district, kind, installed.
The district of a reading is the district of its meter.
"""

import csv

Row = dict[str, str]


def load(path: str) -> list[Row]:
    """Read a CSV file; return one dictionary of strings per data row."""
    with open(path, encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def count_per_meter(readings: list[Row]) -> dict[str, int]:
    """Take the readings; return how many each meter has, by meter id."""
    raise NotImplementedError("step 1: one pass over the readings, one dictionary")


def count_per_district_slow(readings: list[Row], meters: list[Row]) -> dict[str, int]:
    """Take readings and meters; return how many readings each district has.

    This version works. For every reading it walks the list of meters until it finds
    the meter of that reading: a loop inside a loop.
    """
    counts: dict[str, int] = {}
    for reading in readings:
        for meter in meters:
            if meter["meter_id"] == reading["meter_id"]:
                district = meter["district"]
                counts[district] = counts.get(district, 0) + 1
                break
    return counts


def count_per_district(readings: list[Row], meters: list[Row]) -> dict[str, int]:
    """The same result as count_per_district_slow, without a loop inside a loop."""
    raise NotImplementedError("step 2: first build a dictionary from meter id to district")


if __name__ == "__main__":
    readings = load("data/readings_clean.csv")
    meters = load("data/meters.csv")
    per_meter = count_per_meter(readings)
    print(len(per_meter), "meters have readings; M-0001 has", per_meter["M-0001"])
    for district, count in sorted(count_per_district(readings, meters).items()):
        print(f"{district:15} {count}")
