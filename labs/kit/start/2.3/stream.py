"""Add up a large readings file two ways: all rows in a list, or one row at a time."""

import csv
from collections.abc import Iterator


def total_list(path: str) -> float:
    """Read every row into a list, then add up the consumption."""
    with open(path, encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    values = [float(row["consumption_m3"]) for row in rows]
    return sum(values)


def read_values(path: str) -> Iterator[float]:
    """Yield the consumption of each row, one at a time, while the file is open."""
    raise NotImplementedError("step 2: open, loop over the reader, yield one float per row")


def total_stream(path: str) -> float:
    """Add up the consumption without ever holding more than one row."""
    raise NotImplementedError("step 3: sum() takes any iterable, a generator included")


if __name__ == "__main__":
    path = "data/readings_large.csv"
    print("list  :", round(total_list(path), 3))
    print("stream:", round(total_stream(path), 3))
