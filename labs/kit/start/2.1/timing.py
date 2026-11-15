"""Time the two versions of count_per_district on 100,000 rows, and keep the result.

    uv run python timing.py

Writes timings.txt. The numbers differ from machine to machine; the ratio is the point.
"""

import time

import count

readings = count.load("data/readings_large.csv")
meters = count.load("data/meters.csv")
print(len(readings), "readings,", len(meters), "meters")

started = time.perf_counter()
slow = count.count_per_district_slow(readings, meters)
nested = time.perf_counter() - started

started = time.perf_counter()
fast = count.count_per_district(readings, meters)
dictionary = time.perf_counter() - started

assert slow == fast, "the two versions must give the same counts"
lines = [f"nested: {nested:.3f}", f"dictionary: {dictionary:.3f}", f"ratio: {nested / dictionary:.0f}"]
print("\n".join(lines))
with open("timings.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(lines) + "\n")
