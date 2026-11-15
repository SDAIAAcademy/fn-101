"""Measure the peak memory of the two totals, and keep the result.

    uv run python memory.py

tracemalloc counts the memory Python allocates while a piece of code runs. Writes memory.txt.
"""

import tracemalloc

import stream

PATH = "data/readings_large.csv"


def peak_of(function) -> tuple[float, int]:
    tracemalloc.start()
    result = function(PATH)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak


list_total, list_peak = peak_of(stream.total_list)
stream_total, stream_peak = peak_of(stream.total_stream)
assert abs(list_total - stream_total) < 1e-6, "the two totals must agree"
lines = [f"list peak: {list_peak / 1024:.0f} KiB",
         f"stream peak: {stream_peak / 1024:.0f} KiB",
         f"ratio: {list_peak / stream_peak:.0f}",
         f"total: {stream_total:.3f} m3"]
print("\n".join(lines))
with open("memory.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(lines) + "\n")
